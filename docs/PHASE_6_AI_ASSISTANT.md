# Phase 6 - AI Assistant

Date: 2026-06-07
Status: Done for local grounded AI MVP

## Goal

Phase 6 adds an AI consultation assistant for the public website and an admin
surface for knowledge base and conversation monitoring.

The assistant is intentionally conservative. It helps customers ask about Ford
model groups, reference prices, on-road estimates, installment estimates and
common questions. It does not close sales or make official commitments.

## Implemented Public Routes And APIs

| Route | Purpose |
| --- | --- |
| `/tro-ly-ai` | Public AI assistant page with chat, source display and handoff form. |
| `/api/ai/chat` | Receives a question, retrieves approved documents, runs tools and logs messages. |
| `/api/ai/handoff` | Converts an AI conversation into a lead for anh Huy. |
| `/api/ai/feedback` | Stores simple message feedback for future review. |
| `/admin/ai` | Admin AI dashboard, KB seed action, docs table and conversation list. |

`/tro-ly-ai` is included in sitemap and primary navigation.

## Provider Strategy

Current provider:

```text
AI_PROVIDER=gemini
AI_MODEL=gemini-2.5-flash-lite
```

Gemini is used only after the internal safety layers have run. The service
still implements:

- System prompt rules.
- Approved knowledge base.
- Keyword retrieval.
- Guardrails.
- Calculator tools.
- Handoff to lead.
- Chat logging.
- Feedback storage.
- Quota fallback.

The selected default model is `gemini-2.5-flash-lite` because the official
Google AI pricing page lists it as cheaper than newer Flash-Lite options for
paid text input/output. Free-tier and paid-tier rate limits still depend on the
Google AI Studio project/tier, so the app keeps `AI_DAILY_QUOTA` as a local
traffic brake.

Runtime behavior:

- Calculator and guardrail answers do not call Gemini.
- Gemini receives only the retrieved approved documents, not the full database.
- API keys are sent through the `x-goog-api-key` header, not in the URL.
- If Gemini errors, times out, returns no usable text or trips unsafe answer
  patterns, the service falls back to the internal grounded answer.
- `/api/ai/chat` returns `provider_name` so deploy smoke tests can confirm
  whether a response came from `gemini:gemini-2.5-flash-lite` or `internal`.
- `.env.example` is read before `.env` for local convenience because the current
  key was placed there. Before Git/deploy, move real secrets into `.env` or host
  environment variables and keep `.env.example` as a template only.

## System Prompt

The system prompt lives in:

```text
app/services/ai_service.py
```

Core behavior:

- Answer only from approved documents, structured data or internal tools.
- Do not finalize price.
- Do not confirm stock, color availability or delivery timeline.
- Do not accept deposit or hold-car requests.
- Do not promise loan approval.
- Do not handle complaints as a final authority.
- Handoff to anh Huy when a question needs official confirmation.

## Knowledge Base

AI documents are stored in:

```text
ai_documents
```

Seed source:

```text
app/data/site_content.py
```

Seed action:

```text
POST /admin/ai/seed
```

Seed includes:

- AI answer rules.
- Handoff policy.
- Anh Huy contact profile.
- Vehicle summaries and reference prices.
- Promotion notes.
- FAQ answers.

Each document stores:

- Title.
- Body.
- Source URL.
- Source updated date.
- Owner.
- Approval status.
- Freshness status.
- Risk level.

## Retrieval Flow

```text
User asks a question
  -> AI service logs user message
  -> Approved and fresh AI documents are token-scored
  -> Top documents are selected as sources
  -> Tool detection runs for on-road or loan questions
  -> Guardrail detection checks high-risk sales intents
  -> Assistant answer is logged with source IDs, tool name and risk flags
```

The retrieval is simple by design for the MVP. It is deterministic, cheap and
safe. A vector store can be added later if the approved document set becomes
large.

## Tools

Implemented tools:

- `on_road_calculator`
- `loan_calculator`

The calculator outputs are explicitly estimates. Loan output is not a bank
approval commitment.

## Guardrails

Current risk flags:

```text
final_price
stock
deposit
loan_approval
complaint
quota_exceeded
```

When risk flags are present, the assistant asks for handoff to anh Huy instead
of inventing a commitment.

## Handoff Flow

```text
Customer chats with AI
  -> Customer submits name, phone, vehicle and area
  -> /api/ai/handoff creates a lead with need_type=ai_handoff
  -> Lead note includes a short AI transcript
  -> Conversation status becomes lead_created
  -> Audit log records ai.handoff
```

## Database Changes

Migration:

```text
alembic/versions/20260607_0003_phase6_ai_assistant.py
```

New tables:

- `ai_documents`
- `ai_conversations`
- `ai_messages`
- `ai_feedback`

## UI Direction

The visual pass follows the Taste Skill direction from:

- https://www.tasteskill.dev/

Applied decisions:

- Public AI page uses an asymmetric hero and console-style AI panel.
- Chat messages have tactile entry motion and source chips.
- Admin AI remains a dense product UI, not a decorative landing page.
- Motion is used for state and focus, with reduced-motion fallback.
- Existing route slugs, public IA, form names and brand wordmark are preserved.

## Validation Completed

Commands:

```powershell
npm run css:build
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m ruff check app tests
.\.venv\Scripts\python.exe -m pytest -q
```

Result:

- CSS build passed.
- Alembic Phase 6 migration applied locally.
- Ruff passed.
- Pytest passed: 10 tests.
- Tests cover AI page route, AI chat calculator, guardrails, handoff lead
  creation, admin AI seed and admin AI dashboard.

## Known Limits

- Gemini is called for grounded, non-guardrail questions when `AI_PROVIDER=gemini`
  and a valid key is configured.
- Retrieval is keyword-based, not vector search.
- Quota is simple daily message count via `AI_DAILY_QUOTA`.
- Public FAQ/promotions still render from Phase 4 seed data, while AI KB uses
  seeded `ai_documents`.
- AI responses must be reviewed during UAT before launch.
