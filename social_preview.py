"""Patches Streamlit's served HTML so link previews (WhatsApp, X, etc.) show
the app's own title/description instead of the generic "Streamlit" defaults.

Chat apps generate link previews by fetching the URL and reading the raw
<head> markup - they do not execute JavaScript. Streamlit is a
single-page app whose only server-rendered HTML is its static index.html,
and `st.set_page_config` only updates `document.title` client-side, so
crawlers still see Streamlit's shipped title/meta tags. Rewriting that
static file's <head> is the only way to control what link previews show.
"""

import re
from pathlib import Path

import streamlit as st

APP_TITLE = "Nigeria Development Simulator"
APP_DESCRIPTION = (
    "Explore how Nigeria's states could invest their budgets: model "
    "population, budgets, and project costs across all 36 states + FCT."
)

_MARKER = "<!-- nigeria-dev-simulator-social-preview -->"


def inject_open_graph_tags() -> None:
    """Rewrite Streamlit's static index.html with our own title/OG tags."""
    try:
        index_html = Path(st.__file__).parent / "static" / "index.html"
        html = index_html.read_text(encoding="utf-8")
    except OSError:
        return

    if _MARKER in html:
        return

    html = re.sub(r"<title>.*?</title>", f"<title>{APP_TITLE}</title>", html, count=1)

    meta_tags = "\n".join(
        [
            _MARKER,
            f'<meta name="description" content="{APP_DESCRIPTION}">',
            f'<meta property="og:title" content="{APP_TITLE}">',
            f'<meta property="og:description" content="{APP_DESCRIPTION}">',
            '<meta property="og:type" content="website">',
            '<meta name="twitter:card" content="summary">',
            f'<meta name="twitter:title" content="{APP_TITLE}">',
            f'<meta name="twitter:description" content="{APP_DESCRIPTION}">',
            "</head>",
        ]
    )
    html = html.replace("</head>", meta_tags, 1)

    try:
        index_html.write_text(html, encoding="utf-8")
    except OSError:
        return
