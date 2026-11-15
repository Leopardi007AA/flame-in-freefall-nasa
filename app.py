"""Flame in Freefall - app shell (role A).

Mounts: theme, Flame Lab, AI Copilot, tiles, ranking and the role C tabs.
If C's modules do not exist yet (ui/theme.py, ui/components.py, ui/tabs/*) it uses
the minimal versions in src/ui_fallbacks.py.
"""
import streamlit as st

from src.ai_engine import DEFAULT_MODEL, RateLimiter, answer_question, get_api_key
from src.data_loader import is_mock, load_investigations, load_papers
from src.scoring import rank
from ui.flame_lab import GRAVITY, render as flame_lab

try:
    from ui.theme import apply_theme
except ImportError:
    from src.ui_fallbacks import apply_theme
try:
    from ui.components import stat_tile
except ImportError:
    from src.ui_fallbacks import stat_tile
try:
    from ui.tabs import compare
except ImportError:
    from src.ui_fallbacks import compare
try:
    from ui.tabs import gaps
except ImportError:
    from src.ui_fallbacks import gaps
try:
    from ui.tabs import real_data
except ImportError:
    from src.ui_fallbacks import real_data

st.set_page_config(page_title="Flame in Freefall", page_icon=":fire:", layout="wide")
apply_theme()

# ---------------- session state ----------------
DEFAULTS = {"gravity": "mars", "o2": 30.0, "pressure": 10.2, "flow": 5.0,
            "highlight_ids": [], "chat": []}
for key, value in DEFAULTS.items():
    st.session_state.setdefault(key, value)
if "limiter" not in st.session_state:
    st.session_state["limiter"] = RateLimiter(max_calls=20, min_interval=3.0)

# 1) apply the actions proposed by the AI BEFORE creating the widgets with the same keys
pending = st.session_state.pop("pending_action", None)
if pending:
    for key in ("gravity", "o2", "pressure", "flow"):
        if pending.get(key) is not None:
            st.session_state[key] = pending[key] if key == "gravity" else float(pending[key])
    if pending.get("highlight_ids"):
        st.session_state["highlight_ids"] = pending["highlight_ids"]


@st.cache_data
def get_data():
    return load_investigations()


df = get_data()
scenario = {k: st.session_state[k] for k in ("gravity", "o2", "pressure", "flow")}
ranked = rank(df, scenario)

# ---------------- sidebar ----------------
with st.sidebar:
    st.header("Settings")
    sidebar_key = st.text_input("Gemini API key (only if not configured)", type="password")
    model = st.text_input("Model", value=DEFAULT_MODEL)
api_key = get_api_key(sidebar_key)

# ---------------- header ----------------
st.title("Flame in Freefall")
st.caption("Fire safety, from microgravity to the Moon. "
           "NASA combustion experiments, ranked and explained for the scenario you choose.")
if is_mock(df):
    st.warning("TEST DATA: this table contains MOCK rows, not real data. "
               "It will be replaced with the verified PSI records.")

# ---------------- Flame Lab + Copilot ----------------
col_lab, col_ai = st.columns([3, 2])

with col_lab:
    st.subheader("Flame Lab")
    flame_lab(**scenario)
    st.radio("Gravity", options=list(GRAVITY), horizontal=True, key="gravity",
             format_func=lambda k: f"{GRAVITY[k]['name']} ({GRAVITY[k]['g']} g)")
    st.slider("Oxygen (% O₂)", 21.0, 85.0, step=0.5, key="o2")
    st.slider("Pressure (psia)", 8.0, 20.0, step=0.1, key="pressure")
    st.slider("Airflow (cm/s)", 0.0, 30.0, step=1.0, key="flow")

with col_ai:
    st.subheader("AI Copilot")
    st.caption("Answers only from the table's records and always cites the ids. "
               "Where there is no data, it says so.")
    urls = dict(zip(df["id"].astype(str), df["url_psi"].astype(str)))
    for msg in st.session_state["chat"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["text"])
            if msg.get("actions"):
                st.caption("Actions taken: " + " · ".join(msg["actions"]))
            if msg.get("citations"):
                st.markdown("Sources: " + ", ".join(
                    f"[{c}]({urls[c]})" if urls.get(c, "") not in ("", "<NA>") else c
                    for c in msg["citations"]))
            if msg.get("details"):
                st.caption("Technical details: " + " | ".join(msg["details"]))
            if msg.get("source") == "fallback":
                st.caption("Saved fallback answer (AI unreachable).")

    question = st.chat_input("E.g. “Show me Mars with 30% oxygen and low airflow”")
    if question:
        st.session_state["chat"].append({"role": "user", "text": question})
        allowed, why_not = st.session_state["limiter"].allow()
        if not allowed:
            st.session_state["chat"].append({"role": "assistant", "text": why_not})
        else:
            with st.spinner("The Copilot is checking the records…"):
                result = answer_question(question, df, scenario, api_key, model)
            reply = result["reply"]
            if reply is None:
                st.session_state["chat"].append({
                    "role": "assistant",
                    "text": "I can't give a verified answer to this question. "
                            "Try rephrasing it.",
                    "details": result["problems"]})
            else:
                actions = []
                if reply.gravity:
                    actions.append(f"gravity → {GRAVITY[reply.gravity]['name']}")
                if reply.o2 is not None:
                    actions.append(f"O₂ → {reply.o2:g}%")
                if reply.pressure is not None:
                    actions.append(f"pressure → {reply.pressure:g} psia")
                if reply.flow is not None:
                    actions.append(f"airflow → {reply.flow:g} cm/s")
                if reply.highlight_ids:
                    n = len(reply.highlight_ids)
                    actions.append(f"{n} experiment{'' if n == 1 else 's'} highlighted")
                st.session_state["chat"].append({
                    "role": "assistant", "text": reply.answer, "actions": actions,
                    "citations": reply.citations, "source": result["source"]})
                st.session_state["pending_action"] = reply.model_dump()
        st.rerun()

# ---------------- tiles ----------------
papers = load_papers()
n_mixed = int((df["gravita"] == "mista").sum())
t1, t2, t3, t4 = st.columns(4)
with t1:
    stat_tile("Investigations", str(len(df)), "Rows in the experiments table")
with t2:
    stat_tile("Linked NTRS papers", str(len(papers)) if papers else "—",
              "Papers curated by role B" if papers else "No data yet")
with t3:
    stat_tile("Gravity between 0 and 1 g", str(n_mixed),
              "No measurement declared at 0.16 g or 0.38 g" if n_mixed == 0 else "Mixed-gravity experiments",
              tone="alert" if n_mixed == 0 else "neutral")
with t4:
    stat_tile(f"Average evidence · {GRAVITY[scenario['gravity']]['name']}",
              f"{ranked['score'].mean():.0f}/100", "MODEL score, updates with the scenario")

# ---------------- ranking ----------------
st.subheader("Which experiments matter for this scenario")
st.caption("Relevance score = MODEL (our own weights: gravity 30, oxygen 25, pressure 15, "
           "airflow 10, raw data 10, safety areas 10). Missing data = 0 points.")
view = ranked[["id", "nome", "progetto", "score"]].copy()
view.insert(0, "★", ["★" if i in st.session_state["highlight_ids"] else "" for i in view["id"].astype(str)])
st.dataframe(view, hide_index=True, use_container_width=True,
             column_config={"id": st.column_config.TextColumn("ID"),
                            "nome": st.column_config.TextColumn("Name"),
                            "progetto": st.column_config.TextColumn("Project"),
                            "score": st.column_config.ProgressColumn("Relevance", min_value=0, max_value=100,
                                                                     format="%d")})
with st.expander("Why is it ranked first?"):
    top = ranked.iloc[0]
    st.write(f"**{top['nome']}** — " + " · ".join(top["why"]))

# ---------------- role C tabs ----------------
tab_cmp, tab_gap, tab_real = st.tabs(["Compare", "Gaps", "Real data"])
with tab_cmp:
    compare.render(df, scenario, st.session_state["highlight_ids"])
with tab_gap:
    gaps.render(df, scenario, st.session_state["highlight_ids"])
with tab_real:
    real_data.render({})   # role B + C: tables from data/raw/ (to be connected)

st.caption("Independent project for the NASA Space Apps Challenge, not affiliated with or endorsed "
           "by NASA. The flames are an illustrative rendering, not a physical simulation.")
