from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json
import re
import sys
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
errors = []
pages = sorted(root.glob("*.html"))
page_data = {}


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.current_script = None
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.tags.append((tag, values))
        if tag == "script":
            self.current_script = {"attrs": values, "body": ""}

    def handle_data(self, data):
        if self.current_script is not None:
            self.current_script["body"] += data

    def handle_endtag(self, tag):
        if tag == "script" and self.current_script is not None:
            self.scripts.append(self.current_script)
            self.current_script = None


for page in pages:
    text = page.read_text(encoding="utf-8")
    parser = Parser()
    try:
        parser.feed(text)
    except Exception as exc:
        errors.append(f"{page.name}: parse error {exc}")
        continue

    tags = parser.tags

    def attrs(tag):
        return [values for name, values in tags if name == tag]

    ids = {values.get("id") for _, values in tags if values.get("id")}
    canonicals = [
        values.get("href")
        for values in attrs("link")
        if "canonical" in str(values.get("rel", ""))
    ]
    noindex = any(
        values.get("name") == "robots" and "noindex" in values.get("content", "")
        for values in attrs("meta")
    )
    page_data[page.name] = {
        "ids": ids,
        "canonicals": canonicals,
        "noindex": noindex,
    }

    if len(attrs("title")) != 1:
        errors.append(f"{page.name}: needs one title")
    if len(attrs("h1")) != 1:
        errors.append(f"{page.name}: needs one h1")
    if page.name != "404.html" and not any(
        values.get("name") == "description" for values in attrs("meta")
    ):
        errors.append(f"{page.name}: missing description")
    if page.name != "404.html" and len(canonicals) != 1:
        errors.append(f"{page.name}: needs exactly one canonical")

    for script in parser.scripts:
        if script["attrs"].get("type") == "application/ld+json":
            try:
                data = json.loads(script["body"])
                if data.get("@context") != "https://schema.org" or not data.get("@type"):
                    errors.append(f"{page.name}: invalid Schema.org JSON-LD context/type")
            except Exception as exc:
                errors.append(f"{page.name}: invalid JSON-LD: {exc}")

    for values in attrs("a"):
        href = values.get("href", "")
        if href.startswith("tel:") and not re.fullmatch(r"tel:\+\d{10,15}", href):
            errors.append(f"{page.name}: invalid telephone URI")
        if not href or href.startswith(("mailto:", "tel:", "http:", "https:", "data:")):
            continue
        parsed = urlsplit(href)
        target = page if not parsed.path else root / parsed.path
        if not target.exists():
            errors.append(f"{page.name}: broken local link {href}")
        elif parsed.fragment and target.suffix == ".html":
            target_data = page_data.get(target.name)
            if target_data is None:
                target_text = target.read_text(encoding="utf-8")
                target_parser = Parser()
                target_parser.feed(target_text)
                target_ids = {
                    item.get("id")
                    for _, item in target_parser.tags
                    if item.get("id")
                }
            else:
                target_ids = target_data["ids"]
            if parsed.fragment not in target_ids:
                errors.append(f"{page.name}: broken local fragment {href}")

    for values in attrs("img"):
        src = values.get("src", "")
        if "alt" not in values:
            errors.append(f"{page.name}: img missing alt")
        if not values.get("width") or not values.get("height"):
            errors.append(f"{page.name}: img missing dimensions {src}")
        if src and not src.startswith("data:") and not (root / src).exists():
            errors.append(f"{page.name}: missing image {src}")

    for values in attrs("meta"):
        if values.get("property") == "og:image":
            image = urlsplit(values.get("content", "")).path.lstrip("/")
            if image and not (root / image).exists():
                errors.append(f"{page.name}: missing Open Graph image {image}")

    if page.name != "404.html":
        links = [values.get("href") for values in attrs("a")]
        if "https://wayner84.github.io/tools/" not in links:
            errors.append(f"{page.name}: missing tools link")

for needed in ["robots.txt", "sitemap.xml", "404.html", "assets/css/style.css"]:
    if not (root / needed).exists():
        errors.append(f"missing {needed}")

try:
    tree = ET.parse(root / "sitemap.xml")
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls = {
        node.text.strip()
        for node in tree.findall("sm:url/sm:loc", namespace)
        if node.text
    }
    expected_urls = set()
    for name, data in page_data.items():
        if name == "404.html" or data["noindex"]:
            continue
        expected_urls.update(data["canonicals"])
    if sitemap_urls != expected_urls:
        errors.append(
            "sitemap/canonical mismatch: "
            f"missing={sorted(expected_urls - sitemap_urls)} "
            f"extra={sorted(sitemap_urls - expected_urls)}"
        )
except Exception as exc:
    errors.append(f"invalid sitemap.xml: {exc}")

print(f"Checked {len(pages)} pages")
if errors:
    print("\n".join("ERROR " + error for error in errors))
    sys.exit(1)
print(
    "All structural, fragment, image, metadata, JSON-LD, sitemap, "
    "phone and tools-entry checks passed."
)
