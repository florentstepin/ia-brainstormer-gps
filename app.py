"""
Application IA-BrainStormer GPS
Système complet : Crash Test DUR + Génération + Priorisation + Séquençage
Mode BYOK (Bring Your Own Key) pour déploiement public
"""
import streamlit as st
import json
# Import direct (Structure à plat)
from gps_system import GPSSystem

# --- FONCTION DE RESET (CALLBACK) ---
def reset_app():
    """
    Cette fonction nettoie l'historique mais GARDE la clé API.
    Elle est appelée AVANT le rechargement de la page.
    """
    keys_to_keep = ['step', 'openai_api_key_input'] # On garde la clé API
    
    # On remet l'étape à zéro
    st.session_state.step = 'crash_test'
    
    # On efface tout le reste (résultats, idées, etc.)
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]

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

# Initialisation de l'état de session de base
if 'step' not in st.session_state:
    st.session_state.step = 'crash_test'

# --- SIDEBAR : CONFIGURATION (SÉCURITÉ) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/compass--v1.png", width=50)
    st.title("Configuration")
    
    st.info("🔒 Mode Sécurisé (BYOK)")
    
    # On ajoute une 'key' pour que Streamlit s'en souvienne
    api_key = st.text_input(
        "Votre Clé API OpenAI", 
        type="password", 
        key="openai_api_key_input",
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
    
    # BOUTON RESET SIDEBAR avec CALLBACK
    st.button("🔄 Nouveau Projet", on_click=reset_app, type="secondary")

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
        
        if st.button("Valider et Passer à la Phase G (Génération) ➡️"):
            st.session_state.idee_validee = idee_reformulee
            st.session_state.step = 'generation'
            st.rerun()

# 2. PHASE G : GÉNÉRATION
elif st.session_state.step == 'generation':
    st.markdown("<div class='phase-title'>Phase G : Générateur d'Angles</div>", unsafe_allow_html=True)
    st.write(f"Idée de base : **{st.session_state.idee_validee}**")
    
    if 'phase_g_result' not in st.session_state:
        with st.spinner("Exploration des multivers stratégiques..."):
            result = gps.phase_g_generation(st.session_state.idee_validee)
            st.session_state.phase_g_result = result
            st.rerun()
            
    else:
        angles = st.session_state.phase_g_result.get('angles', [])
        selection = []
        
        st.subheader("Choisissez 3 angles à auditer :")
        
        # Gestion de la sélection multiple
        selected_indices = []
        for i, angle in enumerate(angles):
            with st.expander(f"📐 {angle['titre']}"):
                st.write(f"**Cible :** {angle['cible_precise']}")
                st.write(f"**Opportunité :** {angle['opportunite']}")
                if st.checkbox("Sélectionner cet angle", key=f"chk_{angle['id']}"):
                    selection.append(angle)
        
        if len(selection) != 3:
            st.warning(f"Veuillez sélectionner exactement 3 angles (Actuellement : {len(selection)})")
        else:
            if st.button("Passer à la Phase P (Priorisation) ➡️"):
                st.session_state.angles_selectionnes = selection
                st.session_state.step = 'priorisation'
                st.rerun()

# 3. PHASE P : PRIORISATION
elif st.session_state.step == 'priorisation':
    st.markdown("<div class='phase-title'>Phase P : La Matrice de Conviction</div>", unsafe_allow_html=True)
    
    if 'phase_p_result' not in st.session_state:
        with st.spinner("Calcul des scores (Douleur x4, Unicité x3, Passion x3)..."):
            result = gps.phase_p_priorisation(st.session_state.angles_selectionnes)
            st.session_state.phase_p_result = result
            st.rerun()
            
    else:
        evaluations = st.session_state.phase_p_result.get('evaluations', [])
        reco = st.session_state.phase_p_result.get('recommandation', {})
        
        # Affichage Tableau
        st.table([{
            "Angle": e['titre'], 
            "Douleur (x4)": e['score_douleur'], 
            "Passion (x3)": e['score_alignement'],
            "SCORE TOTAL": e['score_total_pondere']
        } for e in evaluations])
        
        st.success(f"🏆 **Recommandation IA :** L'angle #{reco.get('id_gagnant')} est le meilleur compromis.")
        st.info(f"Pourquoi ? {reco.get('raison')}")
        
        # Le Veto final
        st.markdown("### 👑 Le Choix Final")
        options = {e['id']: e['titre'] for e in evaluations}
        
        # Selectbox simple
        choix_id = st.selectbox("Quel angle choisissez-vous réellement ?", list(options.keys()), format_func=lambda x: options[x])
        
        if st.button("Générer le Plan de Bataille (Phase S) ➡️"):
            # Retrouver l'objet complet de l'angle choisi
            angle_final_obj = next((item for item in st.session_state.angles_selectionnes if item["id"] == choix_id), None)
            st.session_state.angle_choisi = angle_final_obj
            st.session_state.step = 'sequencage'
            st.rerun()

# 4. PHASE S : SÉQUENÇAGE
elif st.session_state.step == 'sequencage':
    st.markdown("<div class='phase-title'>Phase S : Le Plan Backcasting</div>", unsafe_allow_html=True)
    
    if 'phase_s_result' not in st.session_state:
        with st.spinner("Téléchargement du plan depuis le futur (J+7 à J+1)..."):
            result = gps.phase_s_sequencage(st.session_state.angle_choisi)
            st.session_state.phase_s_result = result
            st.rerun()
            
    else:
        plan = st.session_state.phase_s_result
        st.info(f"🏁 **Objectif J+7 :** {plan.get('resultat_j7')}")
        
        for jour in plan.get('etapes_journalieres', []):
            with st.chat_message("assistant"):
                st.write(f"**{jour['jour']} :** {jour['action_principale']}")
                st.caption(f"🎯 Détail : {jour['detail_execution']}")
        
        st.markdown("---")
        
        # Export JSON
        plan_complet = {
            'idee': st.session_state.idee_validee,
            'angle_choisi': st.session_state.angle_choisi,
            'plan_action': plan
        }
        
        col_dl, col_reset = st.columns(2)
        
        with col_dl:
            st.download_button(
                "💾 Télécharger mon Plan GPS (.json)",
                data=json.dumps(plan_complet, indent=4, ensure_ascii=False),
                file_name="mon_plan_gps.json",
                mime="application/json",
                use_container_width=True
            )
            
        with col_reset:
            # BOUTON RESET FINAL avec CALLBACK
            st.button("🔄 Lancer un nouveau projet", on_click=reset_app, type="primary", use_container_width=True)
