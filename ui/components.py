import html

import streamlit as st

# icona e classe CSS per ogni tipo di etichetta di provenienza
BADGES = {
    "real": ("◆", "badge-real"),
    "model": ("▲", "badge-model"),
    "illustrative": ("✦", "badge-illustrative"),
    "nodata": ("○", "badge-nodata"),
}

TONES = ("neutral", "warm", "cool", "alert")


def badge(text: str, kind: str = "real") -> str:
    """Restituisce l'HTML di un'etichetta di provenienza.
    kind: real (ciano, dato misurato) | model (viola, calcolato) |
          illustrative (arancio) | nodata (grigio, nessun dato)"""
    icon, css_class = BADGES.get(kind, BADGES["nodata"])
    return (
        f'<span class="badge {css_class}">'
        f'<span aria-hidden="true">{icon}</span> {html.escape(text)}'
        f"</span>"
    )


def glass_card(title: str, body_html: str, *, accent: str | None = None) -> None:
    """Mostra una card di vetro con titolo e contenuto HTML."""
    style = f' style="border-top: 3px solid {accent};"' if accent else ""
    st.markdown(
        f'<div class="glass"{style}>'
        f'<div class="card-title">{html.escape(title)}</div>'
        f'<div class="card-body">{body_html}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )


def stat_tile(label: str, value: str, note: str = "", tone: str = "neutral") -> None:
    """Tile con etichetta, numero grande e nota.
    tone: neutral | warm | cool | alert.
    La nota può contenere l'HTML di un badge."""
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