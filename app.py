import streamlit as st
import pandas as pd
import plotly.express as px
from src.ai_engine import ask_nasa_ai

# Configurazione Pagina
st.set_page_config(
    page_title="Flame in Freefall | NASA Dashboard",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 Flame in Freefall: Microgravity Fire Safety Dashboard")
st.caption("Analisi dei dati di combustione NASA PSI per la sicurezza antincendio su Luna e Marte")

# --- SIDEBAR: FILTRI & IMPOSTAZIONI ---
st.sidebar.header("⚙️ Filtri Esperimento")

api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Inserisci la tua chiave API di Google AI Studio")

experiment_type = st.sidebar.selectbox(
    "Seleziona Esperimento NASA",
    ["Tutti", "ACME (Gassoso)", "BASS / BASS-II (Solido)", "FLEX (Liquido)", "Saffire"]
)

fuel_state = st.sidebar.multiselect(
    "Stato del Combustibile",
    ["Solido", "Liquido", "Gassoso"],
    default=["Solido", "Gassoso"]
)

o2_concentration = st.sidebar.slider(
    "Concentrazione di Ossigeno (% O₂)",
    min_value=21,
    max_value=85,
    value=30,
    help="Atmosfera standard terrestre: 21%. Basi lunari/rover: ≥30%"
)

airflow_speed = st.sidebar.slider("Velocità Flusso d'Aria (cm/s)", 0, 30, 5)

# --- CORPO PRINCIPALE: LAYOUT A 2 COLONNE ---
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📊 Visualizzazione Dati di Combustione")
    
    # Dataset di esempio per i grafici
    dummy_data = pd.DataFrame({
        "Esperimento": ["BASS-1", "BASS-2", "ACME-1", "ACME-2", "FLEX-1"],
        "Materiale": ["Acrilico", "Cotone", "Metano", "Propano", "Eptano"],
        "O2_Perc": [21, 30, 25, 40, 30],
        "Tempo_Estinzione_sec": [45, 120, 30, 85, 60]
    })
    
    # Grafico interattivo Plotly
    fig = px.bar(
        dummy_data, 
        x="Materiale", 
        y="Tempo_Estinzione_sec", 
        color="O2_Perc",
        title=f"Tempo di Estinzione vs Materiale (Filtro O₂ impostato: {o2_concentration}%)",
        labels={"Tempo_Estinzione_sec": "Tempo Estinzione (s)", "O2_Perc": "% Ossigeno"},
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("ℹ️ Sintesi Tecnica Esperimento Selezionato"):
        st.write(f"""
        - **Esperimento attivo:** {experiment_type}
        - **Parametri impostati:** {o2_concentration}% O₂ | Flusso d'aria: {airflow_speed} cm/s
        - **Note scientifiche:** Ad elevate concentrazioni di ossigeno (≥30%), la velocità di propagazione della fiamma nei materiali solidi aumenta esponenzialmente in assenza di gravità.
        """)

with col2:
    st.subheader("🤖 NASA Fire Safety AI Assistant")
    
    # Inizializzazione cronologia chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Visualizzazione messaggi precedenti
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input chat
    if user_query := st.chat_input("Fai una domanda sui dati di combustione NASA..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Analisi dei dati NASA PSI in corso..."):
                response_text = ask_nasa_ai(user_query, api_key)
                st.markdown(response_text)
        
        st.session_state.messages.append({"role": "assistant", "content": response_text})