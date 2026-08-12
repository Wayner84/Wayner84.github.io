# Townsend Precision Labs Website Audit

**Audit date:** 12 August 2026

**Repository:** `Wayner84/Wayner84.github.io`

**Production URL:** <https://wayner84.github.io/>

**Scope:** all 22 original HTML pages, shared CSS and image assets; desktop and mobile rendering; navigation and product interactions; accessibility, SEO, performance, privacy, business credibility and deployment hygiene.

## Executive Summary

The site had a sound lightweight static foundation and no broken internal file links, but it looked and behaved more like an early catalogue draft than a finished company website. The most urgent defects were a broken click-to-call URI, public placeholder pricing/content, a privacy notice too thin for the customer and technical information being collected, absent company identity in the footer, and no automated validation. Search/discovery metadata and accessibility were also inconsistent.

The August 2026 remediation keeps the site deliberately simple and fast while improving trust, navigation, conversion and maintainability. The requested tools portal is linked in every primary/mobile/footer navigation and receives a dedicated homepage section.

## Fixed Immediately

### High priority

1. **Broken click-to-call link — fixed**
   - The displayed phone number was valid, but its `tel:` URI contained literal masking characters and could not be dialled.
   - The URI now uses the number derived from the visible public contact number, and validation rejects malformed telephone URIs.

2. **Public placeholder product content — contained**
   - Several pages displayed `£XX.XX`, “Placeholder price”, “Photos to be added” and “Final pricing to be confirmed”. This undermined trust and made draft sizes look sale-ready.
   - Public wording now says `Enquire`, `Quoted per set`, `Pricing confirmed at quote stage` or describes photography as pending final validation.
   - Unfinished standalone pages are marked `noindex, follow`; confirmed products remain indexable.
   - **Still requires a business decision:** final prices and real photography before those variants should be promoted as standard products.

3. **Insufficient privacy information — fixed proportionately**
   - The old two-sentence notice did not explain controller identity, categories of data, purposes/lawful bases, sharing, retention, rights, international processing or ICO recourse.
   - The replacement notice covers enquiry, order, invoice and technical-file handling, while accurately stating that the static site has no first-party analytics, advertising scripts, contact form or cookies.
   - This is an operational notice, not legal advice; it should be reviewed if marketing, analytics, ecommerce, a CRM or a hosted contact form is introduced.

4. **Weak legal/business identity — fixed**
   - The footer now gives the registered company name, Companies House number, registered office and Gloucester/UK context.
   - The contact page links to the Companies House record and makes clear that the registered office is not advertised as walk-in premises.

### Medium priority

5. **No tools route from the company site — fixed**
   - Added `Tools` to desktop and mobile navigation across the site.
   - Added `Free browser tools` to the footer.
   - Added a prominent homepage section explaining the 25-tool portal, its 19 tracked upstreams, public access and provenance.

6. **No search-engine discovery files — fixed**
   - Added canonical links, social/Open Graph metadata, a 16-URL sitemap and `robots.txt`.
   - Added `ProfessionalService` structured data on the homepage.
   - Added a branded `404.html` recovery page.

7. **Missing favicon / browser-console 404 — fixed**
   - Every page now declares the existing logo as its favicon.

8. **Accessibility baseline — fixed**
   - Added skip links, labelled primary/footer navigation, current-page states, discernible brand-link names, visible keyboard focus, minimum button heights, image dimensions, reduced-motion handling and decorative logo treatment.
   - Representative homepage, products, contact, privacy and vee-block pages produce zero automated WCAG A/AA violations in axe-core.

9. **External font dependency — removed**
   - Removed Google Fonts requests. The site now uses system fonts, reducing third-party requests, privacy surface and render dependency.

10. **No regression checks — fixed**
    - Added deterministic validation for 23 pages covering titles, headings, descriptions, canonicals, local links/assets, image alternatives/dimensions, telephone URIs and tools links.
    - Added a minimal-permission GitHub Actions workflow to run it on pull requests and `main` pushes.

## Visual and UX Improvements Implemented

- Strengthened hero hierarchy and made the headline easier to scan.
- Added a secondary `Browse products` action alongside the quote CTA.
- Improved typography, spacing, focus states and button tap targets.
- Promoted the plain featured-products list into a defined panel.
- Added a polished tools callout without displacing the main quote/product journey.
- Added a structured company footer rather than a copyright-only strip.
- Reworked contact information into scannable quote and requirement cards.
- Improved desktop and 390px mobile layouts with no horizontal overflow.
- Preserved the established dark technical aesthetic and magenta logo rather than performing a disruptive rebrand.

## Verification Evidence

- All original internal file references were valid before changes.
- Structural validator: **23 pages checked; all checks passed**.
- HTML validator: passed with the project’s accepted HTML void/doctype style rules disabled.
- Browser smoke tests in headless Microsoft Edge at **1440px and 390px**:
  - no horizontal overflow;
  - no console errors;
  - no failed resources;
  - homepage tools CTA present;
  - contact telephone URI present;
  - height-adjuster selectors update price and photo;
  - vee-block size selector changes enquiry state and preview.
- axe-core WCAG A/AA checks: **0 violations** on representative homepage, products, contact, privacy and vee-block pages.
- `git diff --check`: passed.
- Lighthouse could not be run because its Windows Chrome launcher did not recognise the installed Edge binary; this was not substituted with invented scores. Direct Playwright/Edge, resource, interaction and axe checks were used instead.

## Work Needed Next

### ASAP: business/content inputs

1. **Replace draft product variants with finished listings**
   - Confirm prices for 45/55/65/75 mm vee blocks and soft-jaw families.
   - Validate specifications and availability before changing `Enquire` to a purchase-ready price.
   - Add real product photography for every promoted standard product.

2. **Build credible proof**
   - The site still lacks finished case studies, testimonials, customer logos or outcome evidence.
   - Replace the unpromoted placeholder portfolio with 2–4 consented case studies: problem, constraints, solution, measurable result and photographs.
   - Do not invent testimonials or publish customer work without permission.

3. **Use a business-domain email**
   - The public Hotmail address works, but an address on a company-controlled domain would improve trust and brand continuity.
   - This depends on selecting/configuring a domain and mailbox; do not remove the working address until delivery is verified.

4. **Decide on a proper company domain**
   - `townsendprecisionlabs.com` did not resolve during this audit; the public site currently uses the personal GitHub Pages URL.
   - A short company domain with HTTPS and verified redirects would improve credibility, memorability and SEO ownership.

### Near term

5. **Product-page consolidation**
   - The repository has repeated headers, footers and metadata across standalone HTML files. This is now validated, but remains expensive to maintain.
   - Move to a small static generator or deterministic include/build step before the catalogue grows significantly.

6. **Quote intake improvement**
   - Email and WhatsApp are appropriate low-friction channels today.
   - If enquiry volume grows, add a privacy-reviewed form with file upload, consent wording, spam controls, secure storage and a documented retention path. Do not bolt on an opaque free form service without reviewing data handling.

7. **Product information consistency**
   - Establish a common template for price basis, VAT status if applicable, shipping, lead time, material, tolerances, intended use, limitations, compatibility and warranty/returns.
   - Add clear commercial terms before enabling direct ecommerce.

8. **Image production**
   - Adopt a repeatable image standard: neutral background, consistent aspect ratio, scale cue, working/application shot and compressed WebP/JPEG variants.
   - Existing JPEG sizes are reasonable, but responsive `srcset`/WebP can be added when the photo library grows.

### Later / strategic

9. **Conversion measurement**
   - The site intentionally has no analytics. If measurement is needed, define the questions first (quote clicks, product interest, tools referrals), then select a privacy-conscious approach and update the notice.

10. **Search/content strategy**
    - Add genuinely useful pages around CMM fixture design, inspection setup aids, additive-manufacturing tolerance expectations and metrology workstation support.
    - Keep tools resources as a useful trust/discovery layer, but do not let general developer-tool traffic obscure the primary engineering offer.

11. **Commercial/legal maturity**
    - Before online purchasing, publish reviewed terms covering quotes, payment, delivery, cancellations/returns, custom-made goods, IP/confidentiality, warranty, acceptable use and liability.
    - Review product compatibility wording and documentation as the CMM accessory range expands.

12. **Deployment modernisation**
    - GitHub Pages currently uses legacy branch deployment. It is functioning and HTTPS-enforced.
    - A workflow artifact deployment would provide more explicit build/deploy gates, but is not urgent while the source is intentionally static and validation runs separately.

## Areas Deliberately Not Changed

- No customer proof, performance claims, certifications, tolerances, lead times or prices were invented.
- No analytics, third-party form, cookie banner or marketing scripts were added.
- Draft product pages were not deleted because they may support ongoing product development; instead they were made honest and excluded from indexing where appropriate.
- The company identity and dark technical design were refined, not replaced.
