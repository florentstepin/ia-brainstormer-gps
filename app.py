"""
Application IA-BrainStormer GPS
Système complet : Crash Test DUR + Génération + Priorisation + Séquençage
Mode BYOK (Bring Your Own Key) pour déploiement public
"""
import streamlit as st
import json
# CORRECTION MAJEURE : Import direct (pas de "utils.")
from gps_system import GPSSystem

# Configuration de la page
st.set_page_config(
    page_title="IA-BrainStormer GPS",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .phase-title {
        font-size: 2rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #667eea;
    }
    .verdict-vert {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
    }
    .verdict-rouge {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation de l'état de session
if 'step' not in st.session_state:
    st.session_state.step = 'crash_test'
if 'history' not in st.session_state:
    st.session_state.history = {}

# --- SIDEBAR : CONFIGURATION (SÉCURITÉ) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/compass--v1.png", width=50)
    st.title("Configuration")
    
    st.info("🔒 Mode Sécurisé (BYOK)")
    
    api_key = st.text_input(
        "Votre Clé API OpenAI", 
        type="password", 
        help="Commence par sk-... Votre clé n'est pas stockée."
    )
    
    model_choice = st.selectbox(
        "Modèle IA", 
        ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 🧭 Étapes")
    st.progress(0 if st.session_state.step == 'crash_test' else 
                33 if st.session_state.step == 'generation' else 
                66 if st.session_state.step == 'priorisation' else 100)
    
    if st.button("🔄 Reset / Nouveau Projet"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- VÉRIFICATION DE LA CLÉ ---
if not api_key:
    st.markdown("<h1 class='main-title'>🧭 IA-BrainStormer GPS</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 👋 Bienvenue Architecte")
        st.write("Ce système transforme vos idées floues en plans d'action concrets.")
        st.write("Pour commencer, vous devez configurer votre 'Moteur' (Clé API).")
        
        st.warning("⬅️ Veuillez entrer votre clé API OpenAI dans la barre latérale.")
        
    with col2:
        with st.expander("🚀 Comment obtenir une clé ?", expanded=True):
            st.write("""
            1. Allez sur [platform.openai.com](https://platform.openai.com/api-keys)
            2. Créez un compte ou connectez-vous.
            3. Cliquez sur **"Create new secret key"**.
            4. Copiez la clé (`sk-...`) et collez-la à gauche.
            """)
    
    st.stop()

# Initialisation du système
gps = GPSSystem(api_key=api_key, model=model_choice)

# --- APPLICATION PRINCIPALE ---

st.markdown("<h1 class='main-title'>🧭 IA-BrainStormer GPS</h1>", unsafe_allow_html=True)

# 1. PHASE 0 : CRASH TEST D.U.R.
if st.session_state.step == 'crash_test':
    st.markdown("<div class='phase-title'>Phase 0 : Le Crash Test D.U.R.</div>", unsafe_allow_html=True)
    st.info("L'Architecte ne construit pas sur du sable. Vérifions la solidité de votre idée.")
    
    idee_initiale = st.text_area(
        "Quelle est votre idée de projet ?", 
        height=150,
        placeholder="Ex: Je veux lancer une formation sur la productivité pour les comptables..."
    )
    
    if st.button("🚀 Lancer le Crash Test"):
        if not idee_initiale:
            st.error("Veuillez décrire votre idée.")
        else:
            with st.spinner("L'Avocat du Diable analyse votre idée..."):
                result = gps.crash_test_dur(idee_initiale)
                st.session_state.crash_test_result = result
                st.session_state.idee_initiale = idee_initiale
                st.rerun()

    if 'crash_test_result' in st.session_state:
        res = st.session_state.crash_test_result
        
        # Affichage des jauges
        c1, c2, c3 = st.columns(3)
        c1.metric("Douleur (Pain)", f"{res.get('score_D', 0)}/10")
        c2.metric("Urgence", f"{res.get('score_U', 0)}/10")
        c3.metric("Reconnu", f"{res.get('score_R', 0)}/10")
        
        if res.get('verdict') == 'VERT':
            st.markdown(f"<div class='verdict-vert'>✅ <b>FEU VERT</b> : {res.get('analyse_critique')}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='verdict-rouge'>🛑 <b>FEU ROUGE</b> : {res.get('analyse_critique')}</div>", unsafe_allow_html=True)
            st.warning(f"💡 Conseil de l'Architecte : {res.get('conseil_architecte')}")

        st.markdown("### ✍️ Le Veto de l'Architecte")
        st.write("Avant de passer à la génération, reformulez votre idée en tenant compte du conseil ci-dessus.")
        
        idee_reformulee = st.text_area(
            "Idée validée pour la suite :", 
            value=st.session_state.get('idee_validee', st.session_state.idee_initiale),
            height=100
        )
        
        if st.button
