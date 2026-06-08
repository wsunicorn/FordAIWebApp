# Phase 2 - UX/UI Direction

Date: 2026-06-07
Status: Done for design/spec phase

## Goal

Turn the current concept into a build-ready UX/UI direction for a personal Ford consultation website for anh Huynh Dang Huy, Tu Van Ban Hang at Dong Thap Ford.

The site is not an online car store. It helps buyers:

- Browse Ford models and variants.
- Check source-backed reference prices and promotions.
- Estimate on-road cost and loan scenarios.
- Ask an AI assistant for approved information.
- Contact anh Huy by phone, Zalo, form, email or Facebook for final confirmation.

## Inputs Reviewed

- User pasted HTML concept: Ford Everest immersive detail page.
- Existing project docs: `PRODUCT.md`, `DESIGN.md`, Phase 0 and Phase 1 docs.
- Local portrait: `assets/images/people/huy-dang-huy.jpg`.
- MVP identity mark: `assets/brand/huy-dang-huy-logo.svg`.
- Source site: https://dongthapford.com/
- Design references saved to `D:\AISkills`.

## Design Read

The website should feel like a premium local automotive advisory desk:

- Human first: anh Huy is visible in the first viewport.
- Vehicle first when browsing models: strong imagery, specs and variant data.
- Data accountable: every price/promotion/calculator value has source and update date.
- Mobile first: call, Zalo and quote CTA are always easy but never block content.
- Polished, not flashy: motion confirms interaction and gives continuity.

## Design Dials

| Dial | Value | Direction |
| --- | --- | --- |
| Visual character | 7/10 premium | Automotive, clean, confident, local-trust focused. |
| Motion intensity | 6/10 public, 2/10 admin | Public pages can have image reveal and CTA feedback; admin stays fast. |
| Information density | 6/10 | Enough for comparison, not a catalogue dump. |
| Brand expression | 5/10 | Use custom wordmark and text identity until official media rights are recorded. |
| AI presence | 4/10 | Helpful assistant, not the main brand visual. |

## Public Sitemap

| Route | Purpose | Primary CTA |
| --- | --- | --- |
| `/` | Home, anh Huy profile, featured vehicles, calculators, AI entry | Call, Zalo, request quote |
| `/anh-huy` | Personal sales profile and contact confidence | Contact anh Huy |
| `/xe` | Vehicle listing, filters and quick compare | View detail, compare |
| `/xe/[slug]` | Vehicle detail, variants, specs, source-backed price | Request quote, test drive |
| `/so-sanh` | Compare models/variants | Send comparison to anh Huy |
| `/bang-gia` | Current reference price table with freshness metadata | Confirm price |
| `/du-toan-lan-banh` | On-road cost estimator | Save scenario, contact |
| `/du-toan-tra-gop` | Loan estimator | Request loan consultation |
| `/uu-dai` | Active promotions and conditions | Check promotion |
| `/faq` | Common buyer questions and AI handoff | Ask AI, contact |
| `/lien-he` | Phone, Zalo, email, Facebook, map/source contact | Call/Zalo/form |
| `/lai-thu` | Test-drive request flow | Submit request |
| `/bao-gia` | Quote request flow | Submit quote request |

## Admin Sitemap

| Route | Purpose |
| --- | --- |
| `/admin` | Dashboard: leads, stale data, recent updates |
| `/admin/leads` | Lead list, filters, status and follow-up |
| `/admin/leads/[id]` | Lead detail, notes, next action |
| `/admin/vehicles` | Vehicle and variant content |
| `/admin/prices` | Prices, promotions, effective dates, review due dates |
| `/admin/content` | FAQ/articles/static content |
| `/admin/ai-documents` | AI-approved documents and metadata |
| `/admin/settings` | Sales contact, source URLs, notification settings |
| `/admin/audit-log` | Content update and revalidation log |

## Home Wireframe

1. Sticky header:
   - Wordmark.
   - Links: Xe Ford, Bang gia, Du toan, Uu dai, FAQ.
   - CTAs: Goi anh Huy, Zalo.
2. Hero:
   - Left: anh Huy identity, role, Dong Thap Ford, trust copy, direct CTAs.
   - Right/background: approved vehicle/showroom visual plus portrait module.
   - Price freshness mini badge: "Gia/uu dai tham khao, anh Huy xac nhan truoc khi chot".
3. Quick finder:
   - Select need: gia dinh, ban tai, dich vu, doanh nghiep, xe dien.
   - Show recommended models and contact handoff.
4. Featured vehicles:
   - Territory, Ranger, Everest, Transit, Ranger Raptor, Mustang Mach-E.
   - Each card has price-from, source date, "Xem chi tiet", "Nhan bao gia".
5. Calculators entry:
   - On-road and loan calculators with clear disclaimer.
6. AI assistant entry:
   - Ask about specs, variants, estimated fees.
   - Handoff for final price, stock, loan approval, delivery.
7. Trust/process:
   - Tu van, lai thu, bao gia, ho tro thu tuc.
   - No "mua ngay", no deposit, no checkout.
8. Latest updates:
   - Promotions/articles from source-backed data.
9. Footer:
   - Contact channels, source/freshness note, legal/brand media note.

## Vehicle Listing Wireframe

1. Header with model search and filters.
2. Filter chips:
   - SUV, ban tai, xe thuong mai, xe dien.
   - Seats, budget range, use case.
3. Vehicle cards:
   - Image, model name, price from, update date, key use case.
   - CTAs: detail, compare, quote.
4. Compare tray:
   - Sticky on desktop bottom/right; mobile bottom sheet.
   - Max 3 models/variants.
5. Empty state:
   - "Chua co xe phu hop bo loc nay" plus reset filter and contact anh Huy.

## Vehicle Detail Wireframe

1. Vehicle hero:
   - Large approved vehicle image.
   - Model name, short positioning, source/update badge.
   - CTAs: quote, test drive, call/Zalo.
2. Variant tabs:
   - Version, price, engine, drivetrain, key options.
   - Tabs are scrollable on mobile.
3. Price block:
   - Listed price, source, effective date, review due date.
   - Strong note: final price/promotion confirmed by anh Huy.
4. Specs and features:
   - Grouped by performance, safety, comfort, dimensions.
5. Calculator dock:
   - Pre-filled model/variant.
6. Related content:
   - FAQ, promotion, compare.
7. Sticky mobile CTA:
   - Call, Zalo, quote, AI.

## Calculator Wireframes

### On-road Cost

- Inputs: model, variant, province/registration area, listed price, insurance/options.
- Outputs: estimated total, breakdown, source/update date.
- Actions: save scenario to quote form, contact anh Huy.
- Disclaimer: reference only; fees and promotions can change.

### Loan Estimate

- Inputs: vehicle price, down payment percent/amount, term, interest assumption.
- Outputs: monthly estimate, principal/interest note, total financed.
- Actions: request loan consultation.
- Guardrail: no loan approval claim; anh Huy/bank confirms.

## Form Wireframes

### Quote Form

- Required: name, phone, interested model, area, need type, consent.
- Optional: budget, expected purchase time, contact channel, note.
- Success state: thank you, show phone/Zalo immediately.
- Error state: field-level errors and retry.

### Test Drive Form

- Required: name, phone, model, preferred area/time, consent.
- Note: anh Huy confirms availability and schedule.

## AI Assistant Wireframe

1. Floating entry:
   - Desktop: compact corner button.
   - Mobile: available in bottom CTA, not a constantly pulsing bubble.
2. Panel:
   - Suggested prompts: compare variants, estimate fee, ask promotion condition.
   - Answers cite source date and handoff button.
3. Handoff:
   - "Can gia chot/ton kho/lai suat duyet vay? Gui cho anh Huy."
   - Pre-fill form with conversation context.
4. Fallback:
   - If AI quota/free tier is unavailable, show FAQ search and contact form.

## Component Library MVP

| Component | Notes |
| --- | --- |
| `Header` | Direct call/Zalo, no crowded nav on mobile. |
| `HeroConsult` | Anh Huy identity + portrait + vehicle/showroom visual. |
| `SalesProfile` | Contact confidence and personal intro. |
| `VehicleCard` | Source-backed price, update badge, compare action. |
| `VehicleGallery` | Approved media only, responsive aspect ratio. |
| `VariantTabs` | Exact transition properties, keyboard support. |
| `PriceFreshnessBadge` | Source, effective date, review due. |
| `CalculatorPanel` | Stable layout, no shifting numbers. |
| `QuoteForm` | Mobile-short, consent and validation states. |
| `AIHandoffFAB` | Idle calm state, animate only on interaction/loading. |
| `MobileCTA` | Safe-area aware, no content obstruction. |
| `FooterContact` | Real contact info and source notes. |
| `AdminDataTable` | Fast filters, no decorative motion. |

## Motion System

Use motion to clarify state, not to decorate.

| Interaction | Duration | Easing | Properties |
| --- | ---: | --- | --- |
| Button hover/active | 120-160ms | ease-out | transform, color, box-shadow |
| Tabs/segmented control | 160-220ms | ease-out | transform, opacity, color |
| Tooltip/popover | 125-180ms | ease-out | opacity, transform, transform-origin |
| Drawer/modal | 220-320ms | custom ease-out | transform, opacity |
| Hero/section reveal | 320-520ms | custom ease-out | opacity, transform, clip-path where safe |
| Calculator value update | 120-250ms | spring/ease-out | opacity, transform, number tween |

Token proposal:

```css
:root {
  --ease-out-strong: cubic-bezier(0.23, 1, 0.32, 1);
  --ease-in-out-smooth: cubic-bezier(0.77, 0, 0.175, 1);
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
  --duration-fast: 140ms;
  --duration-base: 220ms;
  --duration-slow: 360ms;
}
```

Rules:

- No `transition-all`.
- No endless `animate-pulse` on AI or CTA.
- Hover scale max 1.03 for cards/images; button active scale 0.97.
- Animate transform/opacity first.
- Large scroll/parallax effects need Playwright screenshot and reduced-motion check.
- Respect `prefers-reduced-motion`: remove parallax, pulse and large movement; keep opacity/color feedback only.

## Production UI Requirements

- Use bundled dependencies, not Tailwind CDN, Google font CDN or duplicated icon links.
- Use `next/font` or self-hosted font assets.
- Use a consistent icon package during implementation.
- Use local/approved media or source-tracked media with permission record.
- Add `alt` text for all vehicle, showroom and portrait images.
- Cards max 8px radius unless there is a deliberate media/gallery reason.
- Do not nest cards inside cards.
- Do not use fake "official dealer" claims unless legally approved.
- Every price/promotion/calculator surface must show source/update date.

## Phase 2 Acceptance

- [x] Public sitemap defined.
- [x] Admin sitemap defined.
- [x] Home, listing, detail, calculator, form and AI wireframes defined.
- [x] Component library MVP defined.
- [x] Design tokens and motion tokens defined.
- [x] Accessibility, responsive, focus and reduced-motion rules defined.
- [x] Pasted design reviewed and improvement actions documented.
