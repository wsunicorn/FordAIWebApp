from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


class SmokeError(RuntimeError):
    pass


def fetch(
    base_url: str,
    path: str,
    *,
    method: str = "GET",
    payload: dict | None = None,
    timeout_seconds: int = 20,
    attempts: int = 1,
    backoff_seconds: int = 0,
) -> tuple[int, str, str]:
    url = urljoin(f"{base_url.rstrip('/')}/", path.lstrip("/"))
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"User-Agent": "ford-ai-smoke/1.0"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    request = Request(url, data=data, headers=headers, method=method)
    retryable_statuses = {429, 502, 503, 504}
    last_error: Exception | None = None

    for attempt in range(1, attempts + 1):
        try:
            with urlopen(request, timeout=timeout_seconds) as response:
                body = response.read().decode("utf-8", errors="replace")
                content_type = response.headers.get("Content-Type", "")
                return response.status, content_type, body
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            if exc.code not in retryable_statuses or attempt == attempts:
                raise SmokeError(f"{method} {url} returned {exc.code}: {body[:240]}") from exc
            last_error = exc
        except (URLError, TimeoutError) as exc:
            if attempt == attempts:
                reason = getattr(exc, "reason", exc)
                raise SmokeError(
                    f"{method} {url} failed after {attempts} attempt(s): {reason}"
                ) from exc
            last_error = exc

        sleep_for = backoff_seconds * attempt
        print(
            f"Retrying {method} {url} in {sleep_for}s "
            f"(attempt {attempt}/{attempts}, last error: {last_error})",
            file=sys.stderr,
        )
        time.sleep(sleep_for)

    raise SmokeError(f"{method} {url} failed unexpectedly")


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise SmokeError(message)


def check_status(status: int, path: str) -> None:
    expect(status == 200, f"{path} returned {status}, expected 200")


def run_smoke(
    base_url: str,
    *,
    check_db: bool,
    submit_lead: bool,
    attempts: int,
    timeout_seconds: int,
    backoff_seconds: int,
) -> list[str]:
    base = base_url.rstrip("/")
    is_local_base = "127.0.0.1" in base or "localhost" in base
    results: list[str] = []

    status, _, body = fetch(
        base,
        "/api/health",
        attempts=attempts,
        timeout_seconds=timeout_seconds,
        backoff_seconds=backoff_seconds,
    )
    check_status(status, "/api/health")
    health = json.loads(body)
    expect(health.get("ok") is True, "/api/health did not return ok=true")
    results.append("health ok")

    if check_db:
        status, _, body = fetch(
            base,
            "/api/health/db",
            attempts=attempts,
            timeout_seconds=timeout_seconds,
            backoff_seconds=backoff_seconds,
        )
        check_status(status, "/api/health/db")
        db_health = json.loads(body)
        expect(db_health.get("ok") is True, "/api/health/db did not return ok=true")
        results.append("database ok")

    status, _, home = fetch(base, "/")
    check_status(status, "/")
    expect("/assets/brand/huy-dang-huy-logo.svg" in home, "homepage is not using the MVP logo")
    expect("/assets/brand/favicon.svg" in home, "homepage favicon link is missing")
    expect("huy-dang-huy-wordmark.svg" not in home, "homepage still references the old wordmark")
    expect(f'<link rel="canonical" href="{base}/"' in home, "homepage canonical URL is wrong")
    results.append("homepage ok")

    status, content_type, favicon = fetch(base, "/favicon.ico")
    check_status(status, "/favicon.ico")
    expect("image/svg+xml" in content_type, "favicon is not served as SVG")
    expect("<svg" in favicon, "favicon body is not SVG")
    results.append("favicon ok")

    status, content_type, logo = fetch(base, "/assets/brand/huy-dang-huy-logo.svg")
    check_status(status, "/assets/brand/huy-dang-huy-logo.svg")
    expect("image/svg+xml" in content_type, "logo is not served as SVG")
    expect("<svg" in logo, "logo body is not SVG")
    results.append("logo ok")

    status, _, robots = fetch(base, "/robots.txt")
    check_status(status, "/robots.txt")
    expect(f"Sitemap: {base}/sitemap.xml" in robots, "robots.txt sitemap URL is wrong")
    results.append("robots ok")

    status, _, sitemap = fetch(base, "/sitemap.xml")
    check_status(status, "/sitemap.xml")
    expect(f"<loc>{base}/</loc>" in sitemap, "sitemap home URL is wrong")
    if not is_local_base:
        expect(
            "127.0.0.1" not in sitemap and "localhost" not in sitemap,
            "sitemap contains local URL",
        )
    results.append("sitemap ok")

    status, _, admin_login = fetch(base, "/admin/login")
    check_status(status, "/admin/login")
    expect('name="robots" content="noindex,nofollow"' in admin_login, "admin login is not noindex")
    results.append("admin noindex ok")

    if submit_lead:
        now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        payload = {
            "full_name": f"Smoke Test {now}",
            "phone": "0900000008",
            "vehicle_interest": "Ford Territory",
            "area": "Smoke",
            "need_type": "quote",
            "note": f"production smoke test {now}",
        }
        status, _, body = fetch(base, "/api/leads", method="POST", payload=payload)
        check_status(status, "/api/leads")
        lead = json.loads(body)
        expect(lead.get("phone") == payload["phone"], "lead smoke response did not echo phone")
        results.append("lead submission ok")

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke test a Ford AI WebApp deployment.")
    parser.add_argument("base_url", help="Base URL, for example https://example.com")
    parser.add_argument("--check-db", action="store_true", help="Check /api/health/db")
    parser.add_argument("--submit-lead", action="store_true", help="Submit a test lead")
    parser.add_argument("--attempts", type=int, default=1, help="Attempts for cold-start probes")
    parser.add_argument("--timeout", type=int, default=20, help="Per-request timeout in seconds")
    parser.add_argument("--backoff", type=int, default=0, help="Linear backoff in seconds")
    args = parser.parse_args()

    try:
        results = run_smoke(
            args.base_url,
            check_db=args.check_db,
            submit_lead=args.submit_lead,
            attempts=max(1, args.attempts),
            timeout_seconds=max(1, args.timeout),
            backoff_seconds=max(0, args.backoff),
        )
    except SmokeError as exc:
        print(f"SMOKE FAILED: {exc}", file=sys.stderr)
        return 1

    for result in results:
        print(f"OK: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
