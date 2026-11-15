"""src/ui_fallbacks.py - minimal versions of the role C modules (ui/theme.py, ui/components.py,
ui/tabs/*). app.py uses them ONLY if C's real files do not exist yet, so the app always
starts. When C delivers, its modules automatically take the place of these.
"""
from types import SimpleNamespace

import streamlit as st


def apply_theme() -> None:
    st.markdown("<style>.stApp{background:#070b1a;color:rgba(255,255,255,.92)}</style>",
                unsafe_allow_html=True)


def glass_card(title: str, body_html: str, *, accent: str | None = None) -> None:
    st.markdown(f"**{title}**")
    st.markdown(body_html, unsafe_allow_html=True)


def stat_tile(label: str, value: str, note: str = "", tone: str = "neutral") -> None:
    st.metric(label, value)
    if note:
        st.caption(note)


def badge(text: str, kind: str = "real") -> str:
    return f"[{text}]"


def _placeholder(name: str):
    def render(*args, **kwargs):
        st.info(f"“{name}” tab: coming from role C.")
    return SimpleNamespace(render=render)


compare = _placeholder("Compare")
gaps = _placeholder("Gaps")
real_data = _placeholder("Real data")
