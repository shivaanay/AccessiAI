"""Public webpage accessibility scanner using Playwright and axe-core.

This is an educational prototype. It is not a WCAG certification service.
"""
import ipaddress
import socket
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

AXE_URL = "https://cdn.jsdelivr.net/npm/axe-core@4.10.3/axe.min.js"
ALLOWED_SCHEMES = {"http", "https"}

def _host_is_public(hostname: str) -> bool:
    """Return True only when every resolved address is globally routable."""
    host = (hostname or "").strip("[]").lower()
    if not host or host in {"localhost", "localhost.localdomain"}:
        return False
    try:
        # Literal IP addresses do not need DNS resolution.
        addresses = [ipaddress.ip_address(host)]
    except ValueError:
        try:
            records = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
            addresses = [ipaddress.ip_address(record[4][0]) for record in records]
        except (socket.gaierror, ValueError):
            return False
    return bool(addresses) and all(address.is_global for address in addresses)

def validate_public_url(raw_url: str) -> str:
    """Normalize and validate a public HTTP(S) URL before scanning."""
    value = (raw_url or "").strip()
    if not value:
        raise ValueError("Enter a webpage URL to scan.")
    parsed = urlparse(value if "://" in value else f"https://{value}")
    if parsed.scheme not in ALLOWED_SCHEMES or not parsed.hostname:
        raise ValueError("Enter a valid http or https webpage address.")
    if parsed.username or parsed.password:
        raise ValueError("URLs containing usernames or passwords are not supported.")
    if not _host_is_public(parsed.hostname):
        raise ValueError("This address is unavailable or points to a local/private network.")
    return parsed.geturl()

def scan_page(raw_url: str) -> dict:
    """Run axe-core against a public page and return summarized findings."""
    url = validate_public_url(raw_url)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1365, "height": 900})

        def guard_request(route):
            # Re-check every navigation/resource, including redirects, to reduce SSRF risk.
            request_url = urlparse(route.request.url)
            if request_url.scheme not in ALLOWED_SCHEMES or not _host_is_public(request_url.hostname):
                route.abort("blockedbyclient")
                return
            route.continue_()

        page.route("**/*", guard_request)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=25000)
            page.add_script_tag(url=AXE_URL)
            result = page.evaluate(
                """async () => await axe.run(document, {
                    runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa']}
                })"""
            )
            violations = []
            for violation in result.get("violations", []):
                nodes = violation.get("nodes", [])
                violations.append({
                    "id": violation.get("id", "unknown"),
                    "impact": violation.get("impact") or "moderate",
                    "description": violation.get("help", "Accessibility issue detected"),
                    "help_url": violation.get("helpUrl", ""),
                    "count": len(nodes),
                    "examples": [
                        {"target": node.get("target", [])[:2],
                         "summary": (node.get("failureSummary") or "")[:500]}
                        for node in nodes[:3]
                    ],
                })
            return {
                "url": page.url, "title": page.title() or page.url,
                "violations": violations,
                "passes": len(result.get("passes", [])),
                "incomplete": len(result.get("incomplete", [])),
            }
        except PlaywrightTimeoutError as exc:
            raise RuntimeError("The page took too long to load. Try another public webpage.") from exc
        finally:
            browser.close()
