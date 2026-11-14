"""Flame in Freefall - guscio dell'app (ruolo A).

Monta: tema, Flame Lab, Copilota AI, tile, ranking e le schede del ruolo C.
Se i moduli di C non esistono ancora (ui/theme.py, ui/components.py, ui/tabs/*) usa
le versioni minime di src/ui_fallbacks.py.
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

# ---------------- stato della sessione ----------------
DEFAULTS = {"gravity": "mars", "o2": 30.0, "pressure": 10.2, "flow": 5.0,
            "highlight_ids": [], "chat": []}
for key, value in DEFAULTS.items():
    st.session_state.setdefault(key, value)
if "limiter" not in st.session_state:
    st.session_state["limiter"] = RateLimiter(max_calls=20, min_interval=3.0)

# 1) applica le azioni proposte dall'AI PRIMA di creare i widget con le stesse chiavi
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
    st.header("Impostazioni")
    sidebar_key = st.text_input("Chiave Gemini (solo se non configurata)", type="password")
    model = st.text_input("Modello", value=DEFAULT_MODEL)
api_key = get_api_key(sidebar_key)

# ---------------- intestazione ----------------
st.title("Flame in Freefall")
st.caption("Sicurezza antincendio: dalla microgravità alla Luna. "
           "Esperimenti NASA sulla combustione, ordinati e spiegati per lo scenario scelto.")
if is_mock(df):
    st.warning("DATI DI PROVA: questa tabella contiene righe MOCK, non dati reali. "
               "Verrà sostituita con i record PSI verificati.")

# ---------------- Flame Lab + Copilota ----------------
col_lab, col_ai = st.columns([3, 2])

with col_lab:
    st.subheader("Flame Lab")
    flame_lab(**scenario)
    st.radio("Gravità", options=list(GRAVITY), horizontal=True, key="gravity",
             format_func=lambda k: f"{GRAVITY[k]['name']} ({GRAVITY[k]['g']} g)")
    st.slider("Ossigeno (% O₂)", 21.0, 85.0, step=0.5, key="o2")
    st.slider("Pressione (psia)", 8.0, 20.0, step=0.1, key="pressure")
    st.slider("Flusso d'aria (cm/s)", 0.0, 30.0, step=1.0, key="flow")

with col_ai:
    st.subheader("Copilota AI")
    st.caption("Risponde solo con i record della tabella e cita sempre gli id. "
               "Dove non ci sono dati lo dice.")
    urls = dict(zip(df["id"].astype(str), df["url_psi"].astype(str)))
    for msg in st.session_state["chat"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["text"])
            if msg.get("actions"):
                st.caption("Azioni eseguite: " + " · ".join(msg["actions"]))
            if msg.get("citations"):
                st.markdown("Fonti: " + ", ".join(
                    f"[{c}]({urls[c]})" if urls.get(c, "") not in ("", "<NA>") else c
                    for c in msg["citations"]))
            if msg.get("source") == "fallback":
                st.caption("Risposta di riserva già salvata (AI non raggiungibile).")

    question = st.chat_input("Es. «Mostrami Marte con 30% di ossigeno e poco flusso»")
    if question:
        st.session_state["chat"].append({"role": "user", "text": question})
        allowed, why_not = st.session_state["limiter"].allow()
        if not allowed:
            st.session_state["chat"].append({"role": "assistant", "text": why_not})
        else:
            with st.spinner("Il Copilota consulta i record…"):
                result = answer_question(question, df, scenario, api_key, model)
            reply = result["reply"]
            if reply is None:
                st.session_state["chat"].append({
                    "role": "assistant",
                    "text": "Non riesco a dare una risposta verificata a questa domanda. "
                            "Riprova con una formulazione diversa."})
            else:
                actions = []
                if reply.gravity:
                    actions.append(f"gravità → {GRAVITY[reply.gravity]['name']}")
                if reply.o2 is not None:
                    actions.append(f"O₂ → {reply.o2:g}%")
                if reply.pressure is not None:
                    actions.append(f"pressione → {reply.pressure:g} psia")
                if reply.flow is not None:
                    actions.append(f"flusso → {reply.flow:g} cm/s")
                if reply.highlight_ids:
                    actions.append(f"{len(reply.highlight_ids)} esperimenti evidenziati")
                st.session_state["chat"].append({
                    "role": "assistant", "text": reply.answer, "actions": actions,
                    "citations": reply.citations, "source": result["source"]})
                st.session_state["pending_action"] = reply.model_dump()
        st.rerun()

# ---------------- tile ----------------
papers = load_papers()
n_mixed = int((df["gravita"] == "mista").sum())
t1, t2, t3, t4 = st.columns(4)
with t1:
    stat_tile("Investigazioni", str(len(df)), "Righe della tabella degli esperimenti")
with t2:
    stat_tile("Articoli NTRS collegati", str(len(papers)) if papers else "—",
              "Articoli curati dal ruolo B" if papers else "Nessun dato ancora")
with t3:
    stat_tile("Gravità tra 0 e 1 g", str(n_mixed),
              "Nessuna misura dichiarata a 0,16 g o 0,38 g" if n_mixed == 0 else "Esperimenti a gravità mista",
              tone="alert" if n_mixed == 0 else "neutral")
with t4:
    stat_tile(f"Evidenza media · {GRAVITY[scenario['gravity']]['name']}",
              f"{ranked['score'].mean():.0f}/100", "Punteggio MODELLO, si aggiorna con lo scenario")

# ---------------- ranking ----------------
st.subheader("Quali esperimenti contano per questo scenario")
st.caption("Punteggio di rilevanza = MODELLO (pesi nostri: gravità 30, ossigeno 25, pressione 15, "
           "flusso 10, dati grezzi 10, aree di sicurezza 10). Dato mancante = 0 punti.")
view = ranked[["id", "nome", "progetto", "score"]].copy()
view.insert(0, "★", ["★" if i in st.session_state["highlight_ids"] else "" for i in view["id"].astype(str)])
st.dataframe(view, hide_index=True, use_container_width=True,
             column_config={"score": st.column_config.ProgressColumn("Rilevanza", min_value=0, max_value=100,
                                                                     format="%d")})
with st.expander("Perché il primo in classifica?"):
    top = ranked.iloc[0]
    st.write(f"**{top['nome']}** — " + " · ".join(top["why"]))

# ---------------- schede del ruolo C ----------------
tab_cmp, tab_gap, tab_real = st.tabs(["Confronto", "Lacune", "Dati reali"])
with tab_cmp:
    compare.render(df, scenario, st.session_state["highlight_ids"])
with tab_gap:
    gaps.render(df, scenario, st.session_state["highlight_ids"])
with tab_real:
    real_data.render({})   # ruolo B + C: tabelle di data/raw/ (da collegare)

st.caption("Progetto indipendente per il NASA Space Apps Challenge, non affiliato né approvato "
           "dalla NASA. Le fiamme sono una resa illustrativa, non una simulazione fisica.")
