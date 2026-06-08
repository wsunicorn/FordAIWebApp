# User Design Review - Phase 2

Date: 2026-06-07
Reviewed input: `C:\Users\Admin\.codex\attachments\1b0fdda9-4248-449a-9ce6-312e4ee5c979\pasted-text.txt`

## Summary

The pasted design has a strong automotive direction: immersive Everest hero, variant tabs, specs grid, cost tools, featured vehicle layout, mobile nav, footer and AI assistant. It is a good visual starting point, but it needs to be converted from a demo-like product page into a trustworthy consultation website for anh Huy.

## What To Keep

| Area | Keep | Reason |
| --- | --- | --- |
| Large vehicle imagery | Keep as a main product/detail pattern | Ford buyers need to inspect real vehicles visually. |
| Variant tabs | Keep and make keyboard/mobile robust | Fits Ford model comparison behavior. |
| Specs grid | Keep with tighter hierarchy | Helps scanning, especially on vehicle detail pages. |
| Calculator section | Keep, but source-back assumptions | High intent lead flow. |
| Featured vehicle bento | Keep in a calmer form | Good for home discovery if prices are current. |
| Sticky mobile actions | Keep, but use safe-area and real labels | Mobile visitors need one-tap contact. |
| AI assistant entry | Keep as support layer | Useful for FAQ and comparison, but not final pricing. |

## Required Improvements

| Current observation | Improvement | Why |
| --- | --- | --- |
| Hero starts as a Ford Everest detail page, not anh Huy's advisory channel. | Home hero must show anh Huy, role, Dong Thap Ford and direct phone/Zalo first. Vehicle detail can be model-first. | The business goal is trust and contact, not direct ecommerce. |
| Header/footer use English labels like `Models`, `Pricing`, `Contact`. | Use Vietnamese-first labels: `Xe Ford`, `Bang gia`, `Du toan`, `Lien he`. | Audience is Vietnamese local buyers. |
| Placeholder phone `0900 123 456` appears. | Replace everywhere with `0766994952`; Zalo `0818655369`; email `hh753741@gmail.com`. | Wrong contact info kills lead flow. |
| Copy says or implies "mua xe", "giao xe tan noi", "hoan hao", "doc quyen", "chinh xac 24/7". | Use consultation copy: "tham khao", "anh Huy xac nhan", "uoc tinh", "nhan bao gia". | Avoid legal/trust risk and AI overclaim. |
| Vehicle prices are inconsistent with source seed in places. | Pull all prices from structured data with source/effective date. | Prevent stale or invented pricing. |
| Footer says official authorized dealer wording. | Say this is anh Huy's personal consultation channel at Dong Thap Ford unless permission/legal wording is recorded. | Avoid official-site confusion. |
| Uses external `lh3.googleusercontent.com/aida-public` images. | Replace with approved/local/source-tracked media. Use placeholders only in internal mockups. | Public site needs rights and stable asset delivery. |
| Tailwind CDN, Google font CDN and duplicated Material Symbols link. | Bundle Tailwind, font and icon dependencies in the app. Use `next/font` or self-host. | Production performance, privacy, reliability and cache control. |
| Heavy `rounded-2xl/3xl`, shadow-heavy cards and decorative blur orbs. | Use tighter radius, quieter depth, full-width sections, cards only for repeated items/tools. | More premium and less generic AI look. |
| Frequent `transition-all`, hover scale 105/110, endless `animate-pulse`. | Animate exact properties, cap image/card scale around 1.03, remove idle pulse. | Smoother, faster, more accessible and less distracting. |
| AI is visually loud and promises too much. | Make AI calm, source-cited and handoff-first for final price/stock/loan. | Trust over spectacle. |
| Bottom nav uses English labels and may block content. | Use Vietnamese labels, safe-area padding, page bottom spacer and route-aware active state. | Better mobile UX. |
| No visible reduced-motion strategy. | Add `prefers-reduced-motion` rules for all motion. | Accessibility and performance. |
| No stale-data state in UI. | Add `PriceFreshnessBadge`, stale warnings and admin review due flow. | Keeps information from becoming outdated. |

## Recommended First View

Desktop:

- Header with wordmark, key links, call/Zalo.
- Hero split or layered layout:
  - Left: "Huynh Dang Huy - Tu Van Ban Hang tai Dong Thap Ford".
  - Subcopy: "Tham khao xe, du toan chi phi va nhan tu van truc tiep."
  - CTAs: `Goi anh Huy`, `Zalo tu van`, `Nhan bao gia`.
  - Freshness note.
  - Right/background: approved Ford vehicle/showroom image plus portrait card using `assets/images/people/huy-dang-huy.jpg`.

Mobile:

- Hero must show identity, phone/Zalo and first CTA before the user scrolls too far.
- Vehicle imagery can sit below the CTA.
- Bottom CTA: `Goi`, `Zalo`, `Bao gia`, `AI`.

## Motion Notes

- Button press: `scale(0.97)` with 120-160ms.
- Tabs: moving indicator and fade under 220ms.
- Image reveal: opacity/clip transform, no layout shift.
- AI typing/loading: subtle only while responding.
- Calculator changes: animate number value without changing card size.
- No scroll hijack.
- No motion on admin keyboard/filter-heavy flows.

## Build Notes For Phase 3

- Start with FastAPI + Jinja2 templates, Tailwind CSS CLI as build dependency, not CDN.
- Use structured vehicle/price seed from Phase 1, not hardcoded demo numbers.
- Replace all demo images with local approved assets or source-tracked image records.
- Add `data-source`, `updated_at`, `effective_to`, `review_due_at` fields before showing price/promotions.
- Add browser checks for desktop/mobile layout, non-overlap, reduced motion and primary CTA visibility.
