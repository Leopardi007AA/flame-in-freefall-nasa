import streamlit as st
from src.ai_engine import genera_modifica_dashboard

st.title("NASA Space Apps - Interactive AI Dashboard")

# Inizializzazione dello stato se non presente
if "config_grafico" not in st.session_state:
    st.session_state["config_grafico"] = {
        "tipo_grafico": "bar",
        "titolo_grafico": "Analisi Dati Iniziale"
    }

# Sidebar per l'interazione con l'AI
with st.sidebar:
    st.header("Assistente AI Modifiche")
    richiesta = st.text_area("Cosa vuoi modificare o aggiungere nella dashboard?")
    if st.button("Applica Modifiche con AI"):
        with st.spinner("Elaborazione modifiche..."):
            risposta = genera_modifica_dashboard(richiesta, st.session_state["config_grafico"])
            
            # Aggiornamento dello stato locale
            st.session_state["config_grafico"]["tipo_grafico"] = risposta.get("tipo_grafico", "bar")
            st.session_state["config_grafico"]["titolo_grafico"] = risposta.get("titolo_grafico", "Grafico")
            
            st.success(risposta.get("spiegazione", "Modifica applicata con successo!"))
            st.rerun()

# Rendering dinamico basato sullo stato aggiornato dall'AI
st.subheader(st.session_state["config_grafico"]["titolo_grafico"])
st.write(f"Tipo di visualizzazione attiva: **{st.session_state['config_grafico']['tipo_grafico']}**")