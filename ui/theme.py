import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ---------- 3.4 SFONDO CON STELLE E LUCI ---------- */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background:
        radial-gradient(circle at 12% 18%, #fff 0, #fff 1.5px, transparent 3px),
        radial-gradient(circle at 28% 72%, #fff 0, #fff 1.5px, transparent 3px),
        radial-gradient(circle at 45% 35%, #fff 0, #fff 2px, transparent 4px),
        radial-gradient(circle at 63% 82%, #fff 0, #fff 1.5px, transparent 3px),
        radial-gradient(circle at 78% 22%, #fff 0, #fff 2px, transparent 4px),
        radial-gradient(circle at 91% 58%, #fff 0, #fff 1.5px, transparent 3px),
        radial-gradient(circle at 6% 90%, #fff 0, #fff 1.5px, transparent 3px),
        radial-gradient(circle at 20% 45%, #fff 0, #fff 1px, transparent 2.5px),
        radial-gradient(circle at 35% 10%, #fff 0, #fff 1.5px, transparent 3px),
        radial-gradient(circle at 52% 62%, #fff 0, #fff 1px, transparent 2.5px),
        radial-gradient(circle at 70% 48%, #fff 0, #fff 1.5px, transparent 3px),
        radial-gradient(circle at 84% 8%, #fff 0, #fff 1px, transparent 2.5px),
        radial-gradient(circle at 96% 88%, #fff 0, #fff 1.5px, transparent 3px),
        radial-gradient(circle at 40% 92%, #fff 0, #fff 1px, transparent 2.5px),
        radial-gradient(circle at 15% 60%, #fff 0, #fff 1px, transparent 2.5px),
        radial-gradient(circle at 58% 15%, #fff 0, #fff 1.5px, transparent 3px),
        radial-gradient(circle at 88% 36%, #fff 0, #fff 1px, transparent 2.5px),
        radial-gradient(circle at 3% 35%, #fff 0, #fff 1.5px, transparent 3px),
        radial-gradient(1200px 700px at 80% -8%, rgba(255,110,50,.22), transparent 62%),
        radial-gradient(900px 700px at 4% 28%, rgba(60,120,255,.22), transparent 62%),
        #070b1a !important;
    background-attachment: fixed !important;
    color: rgba(255,255,255,.92);
    font-family: Inter, sans-serif;
}

header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer { visibility: hidden; }

/* ---------- CARD DI VETRO (classe da usare in HTML) ---------- */
.glass {
    background: linear-gradient(150deg, rgba(255,255,255,.10), rgba(255,255,255,.035));
    border: 1px solid rgba(255,255,255,.14);
    border-radius: 26px;
    padding: 20px;
    backdrop-filter: blur(26px) saturate(150%);
    box-shadow: 0 24px 70px rgba(0,0,0,.4);
    transition: transform .3s ease;
}
.glass:hover { transform: translateY(-4px); }

/* ---------- 3.5 TITOLI, TESTI E CARATTERI ---------- */
h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: rgba(255,255,255,.92) !important;
    letter-spacing: -0.01em;
}
p, li, label, .stMarkdown {
    font-family: Inter, sans-serif;
    color: rgba(255,255,255,.72);
}
.mono-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: rgba(255,255,255,.72);
}

/* ---------- 3.6 SCHEDE (st.tabs) ---------- */
button[data-baseweb="tab"] {
    background: transparent !important;
    color: rgba(255,255,255,.72) !important;
    font-family: 'Space Grotesk', sans-serif;
    transition: color .3s ease;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #ff8a4c !important;
}
[data-baseweb="tab-highlight"] {
    background-color: #ff8a4c !important;
}
[data-baseweb="tab-border"] {
    background-color: rgba(255,255,255,.14) !important;
}

/* ---------- 3.7 PULSANTI ---------- */
.stButton > button,
.stDownloadButton > button,
.stLinkButton > a {
    background: rgba(255,255,255,.07) !important;
    border: 1px solid rgba(255,255,255,.14) !important;
    border-radius: 16px !important;
    color: rgba(255,255,255,.92) !important;
    transition: transform .3s ease, border-color .3s ease;
}
.stButton > button:hover,
.stDownloadButton > button:hover,
.stLinkButton > a:hover {
    border-color: #ff8a4c !important;
    transform: translateY(-4px);
}

/* ---------- 3.7 MENU A TENDINA E SELEZIONE MULTIPLA ---------- */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,.07) !important;
    border: 1px solid rgba(255,255,255,.14) !important;
    border-radius: 14px !important;
    color: rgba(255,255,255,.92) !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] input {
    color: rgba(255,255,255,.92) !important;
}
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li {
    background: #12182b !important;
    color: rgba(255,255,255,.92) !important;
}
div[data-baseweb="popover"] li:hover {
    background: rgba(255,138,76,.18) !important;
}

/* ---------- 3.7 CURSORI ---------- */
[data-testid="stSlider"] [role="slider"] {
    background-color: #ff8a4c !important;
    border-color: #ff8a4c !important;
}

/* ---------- 3.8 CONTENITORI CON BORDO (st.container(border=True)) ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(150deg, rgba(255,255,255,.10), rgba(255,255,255,.035));
    border: 1px solid rgba(255,255,255,.14) !important;
    border-radius: 26px !important;
    padding: 20px;
    backdrop-filter: blur(26px) saturate(150%);
    box-shadow: 0 24px 70px rgba(0,0,0,.4);
    transition: transform .3s ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-4px);
}

/* ---------- 3.9 ACCESSIBILITA' ---------- */
*:focus-visible {
    outline: 2px solid #5ce1e6 !important;
    outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
    * {
        animation: none !important;
        transition: none !important;
    }
    .glass:hover,
    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stLinkButton > a:hover,
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: none !important;
    }
}
</style>
"""


def apply_theme() -> None:
    st.markdown(CSS, unsafe_allow_html=True)