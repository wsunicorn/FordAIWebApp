# Render + Cloudflare Launch Runbook

Updated: 2026-06-08

## Recommendation

Use Render Free for preview/UAT first. Do not treat the free tier as a final
production setup if leads become important. Render's own free-tier docs say free
instances are for testing, hobby projects and previewing the platform, not
production applications.

Recommended first public path:

1. Deploy preview on Render Free: `https://huy-ford-dong-thap.onrender.com`.
2. Run UAT with anh Huy on a real phone.
3. Buy a domain and put DNS on Cloudflare.
4. Add the custom domain to Render.
5. Run smoke tests.
6. Only then enable canonical redirects.

## Domain Choice

Prefer a personal brand domain, not a Ford-like official domain.

Best candidates to check:

- `huydanghuyauto.com`
- `huydanghuyoto.com`
- `huynhdanghuyauto.com`
- `huydanghuydongthap.com`

If budget allows and the name is available, `.vn` can feel more local and
trustworthy in Vietnam:

- `huydanghuyauto.vn`
- `huydanghuyoto.vn`

Avoid domains that imply official Ford ownership, such as:

- `forddongthapofficial...`
- `fordvietnam...`
- anything that looks like Ford corporate property.

## How To Get DNS And Cloudflare Access

You need one of these:

### Option A - Buy Domain At Cloudflare

1. Create/login Cloudflare account.
2. Go to **Domain Registration**.
3. Search the chosen domain.
4. Register it.
5. Cloudflare will automatically use Cloudflare nameservers.

This is the cleanest path if the TLD is supported.

### Option B - Buy Domain Somewhere Else, Use Cloudflare DNS

1. Buy the domain at a registrar such as Namecheap, Porkbun, GoDaddy or a local
   `.vn` registrar.
2. Create/login Cloudflare account.
3. Add the domain to Cloudflare.
4. Cloudflare gives you two nameservers.
5. Go back to the registrar and replace the domain's nameservers with the two
   Cloudflare nameservers.
6. Wait for Cloudflare to mark the domain active.

### If You Want Someone Else To Configure DNS

In Cloudflare:

1. Go to account/team members.
2. Invite their email.
3. Give only the needed permission:
   - `Zone DNS Edit`
   - or zone-level DNS management for this domain.

Do not share your Cloudflare password.

## Render Deploy Steps

1. Push this project to GitHub.
2. Create a Render account.
3. In Render, choose **Blueprint**.
4. Connect the GitHub repo.
5. Render should detect `render.yaml`.
6. Review resources:
   - Web service: `huy-ford-dong-thap`
   - Postgres: `huy-ford-dong-thap-db`
7. Render will ask for secret values marked `sync: false`.
8. Open local file `.env.production.local` and copy values into Render env vars.
9. For `DATABASE_URL`, use Render's database connection string from the Blueprint.
10. Deploy.

Important env vars:

```text
APP_ENV=production
APP_DEBUG=false
APP_URL=https://huy-ford-dong-thap.onrender.com
CANONICAL_REDIRECT=false
SECRET_KEY=<from .env.production.local>
DATABASE_URL=<Render Postgres internal database URL>
REVALIDATION_SECRET=<from .env.production.local>
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<from .env.production.local>
AI_API_KEY=<Gemini key, optional>
GA_MEASUREMENT_ID=<GA4 Measurement ID, optional>
SENTRY_DSN=<Sentry DSN, optional>
```

## Gemini Key

The Gemini key must not live in `.env.example`.

Use one of these:

- Paste the existing Gemini key into `.env.production.local`, then Render
  `AI_API_KEY`.
- Or create a new key in Google AI Studio and use the new value.

If `AI_API_KEY` is empty, the app still runs with the internal grounded fallback.

## GA4 Setup

Use GA4 for traffic and conversion visibility.

1. Go to Google Analytics.
2. Create Account and Property.
3. Create a Web data stream for the final domain.
4. Copy the Measurement ID. It starts with `G-`.
5. Put it into Render as `GA_MEASUREMENT_ID`.
6. Redeploy.
7. Open GA4 Realtime report and visit the site to confirm traffic.

The app already injects the Google tag only when `GA_MEASUREMENT_ID` is set.

## Search Console Setup

Use Google Search Console for SEO/indexing.

1. Go to Google Search Console.
2. Add a **Domain property** for the chosen domain.
3. Google gives a DNS TXT record like:

```text
google-site-verification=...
```

4. Add that TXT record in Cloudflare DNS.
5. Wait for DNS propagation.
6. Click Verify in Search Console.
7. Submit sitemap:

```text
https://<canonical-domain>/sitemap.xml
```

Keep the TXT record after verification.

## Sentry Setup

Use Sentry Developer plan first for errors and one uptime monitor.

1. Create Sentry account.
2. Create a Python/FastAPI project.
3. Copy the DSN.
4. Put it into Render as `SENTRY_DSN`.
5. Keep `SENTRY_TRACES_SAMPLE_RATE=0.1`.
6. Redeploy.
7. Create one uptime monitor for:

```text
https://<public-host>/api/health
```

## Custom Domain On Render

After the domain is active in Cloudflare:

1. In Render service, open **Settings > Custom Domains**.
2. Add:

```text
www.<domain>
```

3. Render tells you what DNS record to add.
4. In Cloudflare DNS, add that record.
5. Wait for Render certificate to become active.
6. After `www` works, decide canonical:
   - Recommended: `https://www.<domain>`
7. Set Render env:

```text
APP_URL=https://www.<domain>
CANONICAL_REDIRECT=true
```

8. Redeploy.

## Post-Deploy Smoke Test

Run:

```powershell
.\.venv\Scripts\python.exe scripts\smoke.py https://<public-host> --check-db
```

When ready to create a real test lead:

```powershell
.\.venv\Scripts\python.exe scripts\smoke.py https://<public-host> --check-db --submit-lead
```

Then log in admin and verify the smoke lead appears.

## What To Send Back To Dev

After doing the account steps, send:

- Render public URL.
- Final domain, if bought.
- Whether canonical should be `www` or apex.
- Whether Gemini is enabled.
- GA4 Measurement ID only if you want it checked in HTML.
- Sentry DSN only if you want it checked, but do not paste it in public chat if
  avoidable.
