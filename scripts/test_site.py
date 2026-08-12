from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json,re,sys
root=Path(__file__).resolve().parents[1]
errors=[]; pages=sorted(root.glob('*.html'))
class P(HTMLParser):
 def __init__(self): super().__init__();self.tags=[]
 def handle_starttag(self,tag,attrs): self.tags.append((tag,dict(attrs)))
for page in pages:
 text=page.read_text(encoding='utf-8'); parser=P();
 try: parser.feed(text)
 except Exception as e: errors.append(f'{page.name}: parse error {e}');continue
 tags=parser.tags
 def attrs(tag): return [a for t,a in tags if t==tag]
 if len(attrs('title'))!=1: errors.append(f'{page.name}: needs one title')
 if len(attrs('h1'))!=1: errors.append(f'{page.name}: needs one h1')
 if not any(a.get('name')=='description' for a in attrs('meta')) and page.name!='404.html': errors.append(f'{page.name}: missing description')
 if page.name!='404.html' and not any(a.get('rel')=='canonical' or 'canonical' in str(a.get('rel','')) for a in attrs('link')): errors.append(f'{page.name}: missing canonical')
 for a in attrs('a'):
  href=a.get('href','')
  if href.startswith('tel:') and not re.fullmatch(r'tel:\+\d{10,15}',href): errors.append(f'{page.name}: invalid telephone URI')
  if not href or href.startswith(('#','http:','https:','mailto:','tel:','data:')): continue
  target=root/urlsplit(href).path
  if not target.exists(): errors.append(f'{page.name}: broken local link {href}')
 for a in attrs('img'):
  if 'alt' not in a: errors.append(f'{page.name}: img missing alt')
  if not a.get('width') or not a.get('height'): errors.append(f'{page.name}: img missing dimensions {a.get("src")}')
  if a.get('src') and not (root/a['src']).exists(): errors.append(f'{page.name}: missing image {a["src"]}')
 if page.name!='404.html':
  links=[a.get('href') for a in attrs('a')]
  if 'https://wayner84.github.io/tools/' not in links: errors.append(f'{page.name}: missing tools link')
for needed in ['robots.txt','sitemap.xml','404.html','assets/css/style.css']:
 if not (root/needed).exists(): errors.append(f'missing {needed}')
print(f'Checked {len(pages)} pages')
if errors:
 print('\n'.join('ERROR '+e for e in errors));sys.exit(1)
print('All structural, link, image, metadata, phone and tools-entry checks passed.')
