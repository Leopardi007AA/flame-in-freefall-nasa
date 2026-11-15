import html

import streamlit as st

# icon and CSS class for each type of provenance label
BADGES = {
    "real": ("◆", "badge-real"),
    "model": ("▲", "badge-model"),
    "illustrative": ("✦", "badge-illustrative"),
    "nodata": ("○", "badge-nodata"),
}

TONES = ("neutral", "warm", "cool", "alert")


def badge(text: str, kind: str = "real") -> str:
    """Returns the HTML of a provenance label.
    kind: real (cyan, measured data) | model (purple, computed) |
          illustrative (orange) | nodata (grey, no data)"""
    icon, css_class = BADGES.get(kind, BADGES["nodata"])
    return (
        f'<span class="badge {css_class}">'
        f'<span aria-hidden="true">{icon}</span> {html.escape(text)}'
        f"</span>"
    )


def glass_card(title: str, body_html: str, *, accent: str | None = None) -> None:
    """Shows a glass card with a title and HTML content."""
    style = f' style="border-top: 3px solid {accent};"' if accent else ""
    st.markdown(
        f'<div class="glass"{style}>'
        f'<div class="card-title">{html.escape(title)}</div>'
        f'<div class="card-body">{body_html}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )


def stat_tile(label: str, value: str, note: str = "", tone: str = "neutral") -> None:
    """Tile with a label, a big number and a note.
    tone: neutral | warm | cool | alert.
    The note may contain the HTML of a badge."""
    if tone not in TONES:
        tone = "neutral"
    note_html = f'<div class="stat-note">{note}</div>' if note else ""
    st.markdown(
        f'<div class="glass stat-tile tone-{tone}">'
        f'<div class="stat-label">{html.escape(label)}</div>'
        f'<div class="stat-value">{html.escape(value)}</div>'
        f"{note_html}"
        f"</div>",
        unsafe_allow_html=True,
    )