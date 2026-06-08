# Design Quality Playbook

This project should use the lessons from:

- https://impeccable.style/
- https://www.tasteskill.dev/
- https://emilkowal.ski/

## Design Read

Brand-led local automotive consultant website with a small product layer. The public website is the main trust surface. The admin dashboard supports the business, but the visitor impression matters first.

## Taste Rules For This Project

### Avoid AI-default visuals

Do not use:

- Generic AI purple/blue gradients.
- Centered hero with vague headline and three feature cards.
- Glassmorphism as default.
- Huge rounded cards everywhere.
- Decorative SVG drawings.
- Stock SaaS phrases.
- Repeated tiny uppercase labels above every section.

### Build trust with specifics

Use:

- Anh Huy's real name and photo.
- Branch context.
- Phone/Zalo visible early.
- Vehicle source and update date.
- Clear "gia tham khao" notes.
- Human handoff copy.

### Make mobile feel native

Use:

- Sticky mobile CTA.
- Large tap targets.
- Short forms.
- Clear loading and success states.
- Horizontal comparison that does not break layout.

## Motion Rules

Follow a purposeful animation decision:

1. Should this animate?
2. What does the animation explain or confirm?
3. Is it frequent or rare?
4. Can it run under 300ms?
5. Does reduced motion work?

Good motion candidates:

- Button press.
- Form submit success.
- AI response loading.
- Drawer/modal.
- Vehicle gallery.

Bad motion candidates:

- Typing into forms.
- Admin table filtering.
- Repeated keyboard actions.
- Decorative loops with no meaning.

## Component Polish Rules

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` | Exact properties like `transform 160ms ease-out` | Avoid accidental slow transitions |
| No active state | `transform: scale(0.97)` on press | Makes buttons feel responsive |
| Popover scales from center | Origin from trigger | Matches spatial expectation |
| Form error shown only at top | Inline error near field | Faster correction on mobile |
| AI answer with no source | Answer with source/freshness note | Builds trust |
| CTA says "Gui" | CTA says "Nhan bao gia" | Clear action and result |

## Public Page Pre-flight

- [ ] First viewport shows who anh Huy is and how to contact him.
- [ ] No ecommerce pattern appears in MVP.
- [ ] CTA hierarchy is not duplicated.
- [ ] Every vehicle/pricing block has source/date note.
- [ ] Typography fits mobile.
- [ ] Body text contrast passes AA.
- [ ] Buttons have tactile feedback.
- [ ] Motion respects reduced motion.
- [ ] Images are real or clearly pending approved assets.
- [ ] AI handoff is obvious.

## Admin Pre-flight

- [ ] Tables are readable.
- [ ] Filters do not reset unexpectedly.
- [ ] Empty states say what to do next.
- [ ] Errors are actionable.
- [ ] Save buttons indicate progress and success.
- [ ] Dangerous actions require confirmation.
- [ ] Audit-sensitive changes are logged.

## Copy Principles

Use plain Vietnamese. Prefer concrete nouns and verbs.

Good labels:

- Nhan bao gia
- Goi anh Huy
- Hoi ve xe nay
- Tinh chi phi du kien
- Dang ky lai thu
- Luu lead

Avoid:

- Mua ngay
- Dat coc
- Thanh toan
- Sieu uu dai
- Gia tot nhat
- Trai nghiem khong gioi han
