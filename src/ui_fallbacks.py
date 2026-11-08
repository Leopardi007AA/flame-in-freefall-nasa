"""src/ui_fallbacks.py - versioni minime dei moduli del ruolo C (ui/theme.py, ui/components.py,
ui/tabs/*). app.py le usa SOLO se i file veri di C non esistono ancora, cosi' l'app parte
sempre. Quando C consegna, i suoi moduli prendono automaticamente il posto di questi.
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
        st.info(f"Scheda «{name}»: in arrivo dal ruolo C.")
    return SimpleNamespace(render=render)


compare = _placeholder("Confronto")
gaps = _placeholder("Lacune")
real_data = _placeholder("Dati reali")
