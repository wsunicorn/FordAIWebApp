# Design

## Design Read

Brand-led local automotive consultant website with a lightweight product/admin layer. Audience is Vietnamese car buyers who need confidence before contacting a real sales consultant. The visual language should feel trustworthy, precise, mobile-first and premium enough for Ford, without copying Ford corporate assets unless approved.

## Visual Direction

The interface should feel like a clean automotive advisory desk, not an ecommerce checkout and not a generic AI landing page.

Preferred qualities:

- Strong first-viewport signal: anh Huỳnh Đang Huy, Tư Vấn Bán Hàng tại Đồng Tháp Ford, direct phone/Zalo contact.
- Real vehicle imagery and real consultant/showroom photos when approved.
- Dense enough for comparison and pricing, but never crowded on mobile.
- Calm confidence: clear type, disciplined spacing, restrained color, strong CTA hierarchy.
- Motion that confirms interaction, not decoration.

Phase 0 brand decisions:

- Use `assets/brand/huy-dang-huy-logo.svg` as the MVP identity mark.
- Do not create a Ford-like logo, Ford oval imitation, or official-looking corporate lockup.
- Display "Đồng Tháp Ford" as text in the sales identity context.
- Use source-site vehicle/showroom/catalogue media only after permission is recorded.

Phase 2 UX/UI decisions:

- First viewport must sell trust in anh Huy before it sells a specific car.
- Product/detail pages may be vehicle-first, but every high-intent surface must keep call/Zalo/quote within reach.
- AI is a support layer, not the visual brand. It should be calm, source-backed and hand off final decisions.
- Premium feel comes from accurate data, real imagery, typography, spacing and restraint, not from heavy gradients or constant animation.
- The pasted Everest HTML is a useful reference for structure, but must be rewritten for production and consultation intent before build.

Design dials:

| Dial | Value | Direction |
| --- | --- | --- |
| Visual character | 7/10 premium | Automotive, local-trust, practical. |
| Motion intensity | 6/10 public, 2/10 admin | Public pages can reveal and guide; admin must stay fast. |
| Information density | 6/10 | Rich enough for comparison, never crowded on mobile. |
| AI presence | 4/10 | Helpful, not dominant. |

## Color Strategy

Use a restrained palette with one primary automotive blue and one action accent.

Recommended tokens:

```css
:root {
  --color-bg: oklch(0.985 0.004 255);
  --color-surface: oklch(1 0 0);
  --color-surface-muted: oklch(0.955 0.008 255);
  --color-ink: oklch(0.19 0.025 260);
  --color-muted: oklch(0.42 0.025 260);
  --color-border: oklch(0.88 0.012 255);
  --color-primary: oklch(0.32 0.12 260);
  --color-primary-strong: oklch(0.24 0.13 260);
  --color-action: oklch(0.62 0.16 38);
  --color-success: oklch(0.58 0.12 150);
  --color-danger: oklch(0.58 0.18 28);
}
```

Rules:

- Do not use purple/blue AI gradients as the brand mechanic.
- Do not make the site mostly beige, cream, brown or coffee-toned.
- Use the action accent only for high-intent actions: call, Zalo, quote request, test drive.
- Body text must meet WCAG AA contrast.

## Typography

Recommended:

- Display/body: `Geist`, `Satoshi`, `Manrope` or a similar clear sans family.
- Mono only for technical metadata such as version, source date, API examples.
- Avoid defaulting to Inter unless the final implementation already uses it.
- Body line length: 65 to 75 characters.
- Headings use scale and weight, not decorative gradient text.

Hierarchy:

- H1: confident but not oversized. Max 2 lines on desktop hero.
- H2: section-level, compact enough for product pages.
- Body: 16px minimum on public pages.
- Form labels and helper text must remain readable on mobile.

## Layout System

Use full-width page sections with constrained inner content. Avoid cards inside cards.

Recommended structure:

- Public pages: top nav, hero/contact strip, vehicle finder, featured models, comparison/calculator entry, AI assistant entry, trust section, latest content, footer contact.
- Vehicle detail: hero image, price/date/source block, variant tabs, specs, cost tools, related articles, sticky mobile CTA.
- Admin: simple product UI with sidebar/topbar, tables, filters, forms and clear empty/error states.

Grid rules:

- Use CSS Grid for vehicle cards and comparison tables.
- Use `repeat(auto-fit, minmax(280px, 1fr))` where possible.
- Avoid three identical feature-card rows unless each card has a real job.

## Components

Core public components:

- Header with direct call/Zalo action.
- Sales profile block.
- Vehicle model card.
- Variant comparison table.
- Price freshness badge.
- Quote request form.
- Test-drive form.
- On-road cost calculator.
- Loan estimate calculator.
- AI assistant panel.
- Lead handoff banner.
- Article card.
- Footer contact block.

Core admin components:

- Lead table.
- Lead detail drawer/page.
- Vehicle editor.
- Price/promotion editor.
- Content editor.
- AI document manager.
- Audit log table.

## Interaction And Motion

Follow these rules from the design-engineering references:

- Buttons need tactile `:active` feedback around `scale(0.97)`.
- UI animations should usually stay under 300ms.
- Use ease-out for entering UI and immediate feedback.
- Avoid `transition: all`; animate exact properties.
- Animate transform and opacity where possible.
- Tooltips/popovers scale from their trigger origin.
- Provide reduced-motion alternatives.

Recommended motion tokens:

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

Production rules:

- Do not use `transition-all`; animate exact properties.
- Do not use endless pulse on the AI button or primary CTA.
- Keep image/card hover scale around 1.01-1.03, never 1.10 for production vehicle cards.
- Use `transform` and `opacity` for most motion.
- Popovers and dropdowns should scale from their trigger origin.
- Respect `prefers-reduced-motion`: remove parallax, continuous motion and large transforms.
- Admin flows that users repeat often should avoid decorative motion.

Motion should support:

- Button press feedback.
- Form success/error transition.
- Drawer/modal open and close.
- Vehicle image/gallery reveal.
- AI response loading state.
- Price/calculator value updates without layout shift.

Motion should not slow:

- Keyboard-driven admin workflows.
- Repeated table filtering.
- Form typing.

## Phase 2 Review Notes

The user-provided HTML concept should be adjusted before implementation:

- Replace placeholder contacts with `0766994952`, `0818655369`, `hh753741@gmail.com` and the confirmed Facebook URL.
- Replace English navigation labels with Vietnamese labels.
- Rewrite ecommerce/official-site copy into consultative copy.
- Pull prices and promotions from structured source-backed data, not hardcoded demo values.
- Replace uncontrolled external image URLs with approved/local/source-tracked assets.
- Remove Tailwind CDN, duplicated font/icon links and any production dependency on demo-hosted assets.
- Reduce rounded corners, nested card feel, oversized shadow and decorative blur orbs.
- Keep mobile bottom actions, but make them safe-area aware and content-safe.

## Imagery

Use real, approved assets as soon as possible:

- Anh Huy portrait.
- Ford Dong Thap showroom or delivery photos.
- Official/approved vehicle images.
- Customer delivery photos only with consent.

Candidate asset:

- `assets/images/people/huy-dang-huy.jpg` can be used for sales profile/hero in MVP.

If assets are not ready, use clear placeholder slots in design files and avoid fake decorative mockups that imply unavailable content.

## Copy Voice

Vietnamese first. Specific, concise and accountable.

Good:

- "Gia tham khao, cap nhat ngay 07/06/2026"
- "Nhan bao gia tu anh Huy"
- "Goi anh Huy: 0766994952"
- "Zalo tu van: 0818655369"
- "Tinh chi phi du kien"
- "Can gia tot nhat? De anh Huy kiem tra va goi lai"

Avoid:

- "Mua ngay"
- "Dat coc online"
- "Gia tot nhat thi truong"
- "AI se tim xe hoan hao cho ban"

## Accessibility Requirements

- All interactive controls reachable by keyboard.
- Visible focus state.
- Form fields have labels, helper text and inline errors.
- CTA text does not wrap awkwardly on desktop.
- Tables can scroll horizontally on mobile with sticky first column when useful.
- Images have meaningful alt text.

## Pre-flight UI Checklist

- [ ] Hero states this is anh Huy's personal advisory channel.
- [ ] No ecommerce checkout pattern in MVP.
- [ ] Primary CTA hierarchy is clear: Call/Zalo, quote, test drive.
- [ ] Vehicle info includes source and update date.
- [ ] Text contrast meets AA.
- [ ] Forms work on mobile with one thumb.
- [ ] Motion has reduced-motion fallback.
- [ ] Empty, loading and error states exist.
- [ ] AI handoff to human is visible and polite.
- [ ] No generic AI/SaaS visual tropes.
