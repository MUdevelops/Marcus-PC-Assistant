"""
commands/media_web.py
Browser and web search commands. Uses the `webbrowser` module, which
opens links in the system default browser — no browser-specific
automation needed.
"""

import webbrowser
import urllib.parse

from logger_setup import get_logger

log = get_logger(__name__)


def open_website(site: str) -> str:
    """Opens a spoken site name/URL in the default browser. Adds
    https:// and .com if the user just said a bare name like 'reddit'."""
    site = site.strip()
    if not site:
        return "I didn't catch which website to open."

    if site.startswith("http://") or site.startswith("https://"):
        url = site
    elif "." in site:
        url = f"https://{site}"
    else:
        url = f"https://{site}.com"

    try:
        webbrowser.open(url)
        log.info("Opened website: %s", url)
        return f"Opening {site}."
    except Exception:
        log.exception("Failed to open website: %s", url)
        return f"I couldn't open {site}."


def search_google(query: str) -> str:
    query = query.strip()
    if not query:
        return "I didn't catch what to search for."
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    try:
        webbrowser.open(url)
        log.info("Google search: %s", query)
        return f"Searching Google for {query}."
    except Exception:
        log.exception("Failed to open Google search.")
        return "I couldn't perform that search."


def search_youtube(query: str) -> str:
    query = query.strip()
    if not query:
        return "I didn't catch what to search for."
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    try:
        webbrowser.open(url)
        log.info("YouTube search: %s", query)
        return f"Searching YouTube for {query}."
    except Exception:
        log.exception("Failed to open YouTube search.")
        return "I couldn't perform that search."
