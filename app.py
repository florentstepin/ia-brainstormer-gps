"""
Application IA-BrainStormer GPS
Système complet : Crash Test DUR + Génération + Priorisation + Séquençage
Mode BYOK (Bring Your Own Key) pour déploiement public
"""
import streamlit as st
import json
from utils.gps_system import GPSSystem

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
    .score-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .tutorial-box {
        background-color: #e7f3ff;
        border-left: 5px solid #2196F3;
        padding: 1.5rem;
        border-radius: 5px;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR : Configuration BYOK
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    # Saisie de la clé API
    api_key = st.text_input(
        "🔑 Entrez votre clé API OpenAI",
        type="password",
        help="Votre clé API OpenAI (commence par sk-...)",
        placeholder="sk-..."
    )
    
    # Sélecteur de modèle
    model_choice = st.selectbox(
        "🧠 Choisissez le modèle",
        ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0,
        help="gpt-4o est recommandé pour la meilleure qualité (~0.05$ par session)"
    )
    
    st.markdown("---")
    
    # Informations sur les coûts
    with st.expander("💰 Estimation des coûts"):
        st.markdown("""
        **Coût approximatif par session complète :**
        - **gpt-4o** : ~0.05$ (Recommandé)
        - **gpt-4-turbo** : ~0.10$
        - **gpt-3.5-turbo** : ~0.01$ (Moins précis)
        
        Une session = Crash Test + 10 angles + Priorisation + Plan de 7 jours
        """)
    
    st.markdown("---")
    
    # Progression (si la clé est entrée)
    if api_key:
        st.markdown("### 📍 Progression")
        
        # Initialisation du session state pour le step
        if 'step' not in st.session_state:
            st.session_state.step = 'crash_test'
        
        steps = {
            'crash_test': '💥 Crash Test D.U.R.',
            'phase_g': '🌟 Phase G : Génération',
            'phase_p': '⚖️ Phase P : Priorisation',
            'phase_s': '🗺️ Phase S : Séquençage',
            'complete': '✅ Plan Complet'
        }
        
        for step_key, step_name in steps.items():
            if st.session_state.step == step_key:
                st.markdown(f"**➡️ {step_name}**")
            else:
                st.markdown(f"{step_name}")
        
        st.markdown("---")
        
        if st.button("🔄 Recommencer", use_container_width=True):
            # Conserver la clé API et le modèle
            api_key_backup = st.session_state.get('api_key_backup', api_key)
            model_backup = st.session_state.get('model_backup', model_choice)
            
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            
            st.session_state.api_key_backup = api_key_backup
            st.session_state.model_backup = model_backup
            st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ À propos")
    st.markdown("Méthodologie **IA-BrainStormer** par Florent")
    st.markdown("🔒 Votre clé n'est pas enregistrée")

# ==========================================
# VÉRIFICATION DE LA CLÉ API
# ==========================================
if not api_key or not api_key.startswith('sk-'):
    # Titre principal
    st.markdown('<h1 class="main-title">🧭 IA-BrainStormer GPS</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Système Génération • Priorisation • Séquençage</p>', unsafe_allow_html=True)
    
    st.warning("⬅️ Veuillez entrer votre clé API OpenAI dans la barre latérale pour commencer.")
    
    # Tutoriel "Zéro Friction"
    st.markdown('<div class="tutorial-box">', unsafe_allow_html=True)
    st.markdown("""
    ### 🚀 Comment utiliser cette application ?
    
    Pour activer le Système GPS, vous avez besoin d'une clé d'accès OpenAI (c'est très simple et peu coûteux).
    
    **1. Obtenez votre Clé :**
    - Allez sur [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
    - Connectez-vous ou créez un compte
    - Cliquez sur "Create new secret key"
    - Copiez la clé (elle commence par `sk-...`)
    
    **2. Activez le GPS :**
    - Collez la clé dans la barre latérale à gauche (🔑)
    - Choisissez le modèle **gpt-4o** pour la meilleure intelligence (coût environ 0.05$ par session complète)
    
    **🔒 Votre clé n'est pas enregistrée.** Elle est utilisée uniquement pour cette session et reste dans votre navigateur.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Démonstration visuelle
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 💥 Crash Test D.U.R.")
        st.info("Validez votre idée selon les critères Douloureux, Urgent, Reconnu")
    
    with col2:
        st.markdown("#### 🌟 Génération")
        st.info("Explorez 10 angles stratégiques pour votre projet")
    
    with col3:
        st.markdown("#### ⚖️ Priorisation")
        st.info("Choisissez le meilleur angle avec la Matrice de Conviction")
    
    st.markdown("---")
    
    st.markdown("#### 🗺️ Séquençage")
    st.info("Obtenez un plan d'action de 7 jours en backcasting")
    
    st.stop()  # Arrête l'exécution tant que la clé n'est pas fournie

# ==========================================
# INITIALISATION DU SYSTÈME GPS
# ==========================================
# Initialisation du session state
if 'step' not in st.session_state:
    st.session_state.step = 'crash_test'
if 'gps_system' not in st.session_state or st.session_state.get('current_model') != model_choice:
    try:
        st.session_state.gps_system = GPSSystem(api_key, model=model_choice)
        st.session_state.current_model = model_choice
    except Exception as e:
        st.error(f"❌ Erreur lors de l'initialisation : {str(e)}")
        st.stop()

if 'crash_test_result' not in st.session_state:
    st.session_state.crash_test_result = None
if 'idee_validee' not in st.session_state:
    st.session_state.idee_validee = None
if 'phase_g_result' not in st.session_state:
    st.session_state.phase_g_result = None
if 'angles_selectionnes' not in st.session_state:
    st.session_state.angles_selectionnes = []
if 'phase_p_result' not in st.session_state:
    st.session_state.phase_p_result = None
if 'angle_choisi' not in st.session_state:
    st.session_state.angle_choisi = None
if 'phase_s_result' not in st.session_state:
    st.session_state.phase_s_result = None

# Titre principal
st.markdown('<h1 class="main-title">🧭 IA-BrainStormer GPS</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Système Génération • Priorisation • Séquençage</p>', unsafe_allow_html=True)

# Badge du modèle utilisé
st.markdown(f'<p style="text-align: center; color: #999;">Modèle actif : <strong>{model_choice}</strong></p>', unsafe_allow_html=True)

# ==========================================
# ÉTAPE 1 : Crash Test D.U.R.
# ==========================================
if st.session_state.step == 'crash_test':
    st.markdown('<div class="phase-title">💥 Phase 0 : Crash Test D.U.R.</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### L'Avocat du Diable
    
    Avant de foncer tête baissée, testons la solidité de votre idée selon la matrice **D.U.R.** :
    - **D**ouloureux : Le problème est-il une souffrance active ?
    - **U**rgent : Y a-t-il un coût immédiat à l'inaction ?
    - **R**econnu : La cible sait-elle qu'elle a ce problème ?
    """)
    
    idee_brute = st.text_area(
        "Décrivez votre idée de projet",
        height=150,
        placeholder="Ex: Une application mobile qui aide les parents TDAH à gérer leur charge mentale quotidienne",
        help="Soyez aussi précis que possible sur le problème que vous voulez résoudre et pour qui"
    )
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("🔍 Lancer le Crash Test", type="primary", use_container_width=True):
            if not idee_brute:
                st.error("❌ Veuillez décrire votre idée")
            else:
                with st.spinner("🤔 L'Avocat du Diable analyse votre idée..."):
                    result = st.session_state.gps_system.crash_test_dur(idee_brute)
                    st.session_state.crash_test_result = result
                    st.session_state.idee_validee = idee_brute
                    st.rerun()
    
    # Affichage des résultats du crash test
    if st.session_state.crash_test_result:
        result = st.session_state.crash_test_result
        
        if "error" in result:
            st.error(f"❌ {result['message']}")
        else:
            st.markdown("---")
            st.markdown("### 📊 Résultats du Crash Test")
            
            # Scores D.U.R.
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div class="score-card">', unsafe_allow_html=True)
                st.metric("Douloureux", f"{result.get('score_D', 0)}/10")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="score-card">', unsafe_allow_html=True)
                st.metric("Urgent", f"{result.get('score_U', 0)}/10")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="score-card">', unsafe_allow_html=True)
                st.metric("Reconnu", f"{result.get('score_R', 0)}/10")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                st.markdown('<div class="score-card">', unsafe_allow_html=True)
                st.metric("Total", f"{result.get('total', 0)}/30")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Verdict
            verdict = result.get('verdict', 'ROUGE')
            verdict_class = 'verdict-vert' if verdict == 'VERT' else 'verdict-rouge'
            verdict_emoji = '✅' if verdict == 'VERT' else '⚠️'
            
            st.markdown(f'<div class="{verdict_class}">', unsafe_allow_html=True)
            st.markdown(f"### {verdict_emoji} Verdict : {verdict}")
            st.markdown(f"**Analyse critique :** {result.get('analyse_critique', 'N/A')}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Maillon faible et conseil
            if 'maillon_faible' in result:
                st.markdown("### 🔧 Conseil de l'Architecte")
                st.info(f"**Maillon faible identifié :** {result['maillon_faible']} ({result['score_maillon_faible']}/10)")
                st.success(f"**Action recommandée :** {result.get('conseil_architecte', 'N/A')}")
            
            # VETO DE L'ARCHITECTE : Zone éditable
            st.markdown("---")
            st.markdown("### ✏️ Veto de l'Architecte")
            st.markdown("Vous pouvez reformuler votre idée en tenant compte des conseils avant de passer à la Phase G.")
            
            idee_modifiee = st.text_area(
                "Idée reformulée (ou gardez l'originale)",
                value=st.session_state.idee_validee,
                height=150,
                help="Modifiez votre idée pour renforcer le maillon faible identifié"
            )
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                if st.button("➡️ Valider et passer à la Phase G", type="primary", use_container_width=True):
                    st.session_state.idee_validee = idee_modifiee
                    st.session_state.step = 'phase_g'
                    st.rerun()

# ==========================================
# ÉTAPE 2 : Phase G - Génération
# ==========================================
elif st.session_state.step == 'phase_g':
    st.markdown('<div class="phase-title">🌟 Phase G : Génération d\'Angles Stratégiques</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### L'Explorateur de Perspective
    
    Nous allons maintenant générer **10 angles stratégiques radicalement différents** pour votre projet.
    Chaque angle aura :
    - Une **cible précise** (niche ultra-spécifique)
    - Une **opportunité** (mécanisme de différenciation et potentiel de monopole)
    """)
    
    st.info(f"**Idée validée :** {st.session_state.idee_validee}")
    
    if not st.session_state.phase_g_result:
        if st.button("🎨 Générer les 10 angles", type="primary", use_container_width=True):
            with st.spinner("🔮 L'Explorateur de Perspective travaille..."):
                result = st.session_state.gps_system.phase_g_generation(st.session_state.idee_validee)
                st.session_state.phase_g_result = result
                st.rerun()
    
    # Affichage des résultats Phase G
    if st.session_state.phase_g_result:
        result = st.session_state.phase_g_result
        
        if "error" in result:
            st.error(f"❌ {result['message']}")
        else:
            st.markdown("---")
            st.markdown("### 🎯 10 Angles Stratégiques Générés")
            
            angles = result.get('angles', [])
            
            if not angles:
                st.warning("⚠️ Aucun angle généré. Veuillez réessayer.")
            else:
                # Affichage des angles avec sélection
                st.markdown("**Sélectionnez vos 3 angles favoris pour la Phase P :**")
                
                for angle in angles:
                    angle_id = angle.get('id', 0)
                    titre = angle.get('titre', 'Sans titre')
                    cible = angle.get('cible_precise', 'N/A')
                    opportunite = angle.get('opportunite', 'N/A')
                    
                    with st.expander(f"**Angle {angle_id} : {titre}**"):
                        st.markdown(f"**🎯 Cible précise :** {cible}")
                        st.markdown(f"**💡 Opportunité :** {opportunite}")
                        
                        # Checkbox pour sélection
                        is_selected = any(a.get('id') == angle_id for a in st.session_state.angles_selectionnes)
                        
                        if st.checkbox(f"Sélectionner cet angle", key=f"select_{angle_id}", value=is_selected):
                            if not is_selected and len(st.session_state.angles_selectionnes) < 3:
                                st.session_state.angles_selectionnes.append(angle)
                        else:
                            if is_selected:
                                st.session_state.angles_selectionnes = [
                                    a for a in st.session_state.angles_selectionnes if a.get('id') != angle_id
                                ]
                
                # Affichage de la sélection
                st.markdown("---")
                st.markdown(f"### ✅ Angles sélectionnés : {len(st.session_state.angles_selectionnes)}/3")
                
                if len(st.session_state.angles_selectionnes) == 3:
                    st.success("Parfait ! Vous avez sélectionné 3 angles.")
                    
                    if st.button("➡️ Passer à la Phase P (Priorisation)", type="primary", use_container_width=True):
                        st.session_state.step = 'phase_p'
                        st.rerun()
                elif len(st.session_state.angles_selectionnes) > 3:
                    st.warning("⚠️ Vous ne pouvez sélectionner que 3 angles maximum.")
                else:
                    st.info(f"ℹ️ Sélectionnez encore {3 - len(st.session_state.angles_selectionnes)} angle(s).")

# ==========================================
# ÉTAPE 3 : Phase P - Priorisation
# ==========================================
elif st.session_state.step == 'phase_p':
    st.markdown('<div class="phase-title">⚖️ Phase P : Priorisation avec la Matrice de Conviction</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### La Matrice de Conviction
    
    Nous allons évaluer vos 3 angles selon la pondération suivante :
    - **Douleur Client** (40%) : Est-ce une "aspirine" ou une "vitamine" ?
    - **Unicité de l'Angle** (30%) : À quel point l'approche est-elle différenciante ?
    - **Alignement/Passion** (30%) : Êtes-vous légitime et passionné par ce sujet ?
    """)
    
    # Affichage des 3 angles sélectionnés
    st.markdown("### 🎯 Vos 3 angles sélectionnés :")
    for i, angle in enumerate(st.session_state.angles_selectionnes):
        with st.expander(f"**Option {i+1} : {angle.get('titre', 'Sans titre')}**"):
            st.markdown(f"**Cible :** {angle.get('cible_precise', 'N/A')}")
            st.markdown(f"**Opportunité :** {angle.get('opportunite', 'N/A')}")
    
    if not st.session_state.phase_p_result:
        if st.button("📊 Lancer l'analyse comparative", type="primary", use_container_width=True):
            with st.spinner("🧮 Calcul de la Matrice de Conviction..."):
                result = st.session_state.gps_system.phase_p_priorisation(st.session_state.angles_selectionnes)
                st.session_state.phase_p_result = result
                st.rerun()
    
    # Affichage des résultats Phase P
    if st.session_state.phase_p_result:
        result = st.session_state.phase_p_result
        
        if "error" in result:
            st.error(f"❌ {result['message']}")
        else:
            st.markdown("---")
            st.markdown("### 📊 Résultats de la Matrice de Conviction")
            
            evaluations = result.get('evaluations', [])
            recommandation = result.get('recommandation', {})
            
            if not evaluations:
                st.warning("⚠️ Aucune évaluation générée. Veuillez réessayer.")
            else:
                # Tableau comparatif
                for eval in evaluations:
                    eval_id = eval.get('id', 0)
                    titre = eval.get('titre', 'Sans titre')
                    score_douleur = eval.get('score_douleur', 0)
                    score_unicite = eval.get('score_unicite', 0)
                    score_alignement = eval.get('score_alignement', 0)
                    score_total = eval.get('score_total_pondere', 0)
                    justification = eval.get('justification', 'N/A')
                    
                    # Vérifier si c'est l'option recommandée
                    is_winner = eval_id == recommandation.get('id_gagnant', 0)
                    
                    with st.expander(f"**{'🏆 ' if is_winner else ''}Option {eval_id} : {titre}** - Score: {score_total}/100", expanded=is_winner):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Douleur Client (40%)", f"{score_douleur}/10")
                        with col2:
                            st.metric("Unicité (30%)", f"{score_unicite}/10")
                        with col3:
                            st.metric("Alignement (30%)", f"{score_alignement}/10")
                        
                        st.markdown(f"**Justification :** {justification}")
                
                # Recommandation
                st.markdown("---")
                st.markdown("### 🏆 Recommandation de l'IA")
                
                id_gagnant = recommandation.get('id_gagnant', 0)
                raison = recommandation.get('raison', 'N/A')
                
                # Trouver l'angle gagnant
                angle_gagnant = next((a for a in st.session_state.angles_selectionnes if a.get('id') == id_gagnant), None)
                
                if angle_gagnant:
                    st.success(f"**Option recommandée :** {angle_gagnant.get('titre', 'Sans titre')}")
                    st.info(f"**Raison :** {raison}")
                    
                    # VETO DE L'ARCHITECTE : Zone éditable
                    st.markdown("---")
                    st.markdown("### ✏️ Veto de l'Architecte")
                    st.markdown("Vous pouvez modifier l'angle recommandé avant de passer à la Phase S.")
                    
                    titre_modifie = st.text_input("Titre", value=angle_gagnant.get('titre', ''))
                    cible_modifiee = st.text_area("Cible précise", value=angle_gagnant.get('cible_precise', ''), height=100)
                    opportunite_modifiee = st.text_area("Opportunité", value=angle_gagnant.get('opportunite', ''), height=150)
                    
                    if st.button("➡️ Valider et passer à la Phase S", type="primary", use_container_width=True):
                        st.session_state.angle_choisi = {
                            'id': id_gagnant,
                            'titre': titre_modifie,
                            'cible_precise': cible_modifiee,
                            'opportunite': opportunite_modifiee
                        }
                        st.session_state.step = 'phase_s'
                        st.rerun()

# ==========================================
# ÉTAPE 4 : Phase S - Séquençage
# ==========================================
elif st.session_state.step == 'phase_s':
    st.markdown('<div class="phase-title">🗺️ Phase S : Séquençage (Plan de Bataille)</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Le Plan de Bataille en Backcasting
    
    Nous allons créer votre plan d'action de **7 jours** en utilisant la méthode du **backcasting** :
    1. Définir le résultat final à J+7
    2. Remonter jour par jour jusqu'à aujourd'hui (J+1)
    """)
    
    st.info(f"**Angle choisi :** {st.session_state.angle_choisi.get('titre', 'N/A')}")
    
    if not st.session_state.phase_s_result:
        if st.button("🗓️ Générer le plan de 7 jours", type="primary", use_container_width=True):
            with st.spinner("📅 Création du plan de bataille..."):
                result = st.session_state.gps_system.phase_s_sequencage(st.session_state.angle_choisi)
                st.session_state.phase_s_result = result
                st.rerun()
    
    # Affichage des résultats Phase S
    if st.session_state.phase_s_result:
        result = st.session_state.phase_s_result
        
        if "error" in result:
            st.error(f"❌ {result['message']}")
        else:
            st.markdown("---")
            st.markdown("### 📅 Votre Plan de Bataille (7 jours)")
            
            resultat_j7 = result.get('resultat_j7', 'N/A')
            plan = result.get('plan', [])
            
            # Résultat final
            st.success(f"**🎯 Résultat à J+7 :** {resultat_j7}")
            
            st.markdown("---")
            
            # Plan jour par jour (de J+7 à J+1)
            if not plan:
                st.warning("⚠️ Aucun plan généré. Veuillez réessayer.")
            else:
                for etape in plan:
                    jour = etape.get('jour', 0)
                    titre = etape.get('titre', 'Sans titre')
                    action_cle = etape.get('action_cle', 'N/A')
                    
                    with st.expander(f"**Jour {jour} : {titre}**", expanded=(jour == 1)):
                        st.markdown(f"**Action clé :** {action_cle}")
                
                # Bouton de finalisation
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Créer un fichier JSON téléchargeable
                    plan_complet = {
                        'idee_initiale': st.session_state.idee_validee,
                        'crash_test': st.session_state.crash_test_result,
                        'angle_choisi': st.session_state.angle_choisi,
                        'plan_action': result
                    }
                    
                    st.download_button(
                        label="📥 Télécharger le plan (JSON)",
                        data=json.dumps(plan_complet, indent=2, ensure_ascii=False),
                        file_name="ia-brainstormer-gps-plan.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with col2:
                    if st.button("✅ Marquer comme terminé", type="primary", use_container_width=True):
                        st.session_state.step = 'complete'
                        st.rerun()

# ==========================================
# ÉTAPE 5 : Terminé
# ==========================================
elif st.session_state.step == 'complete':
    st.markdown('<div class="phase-title">✅ Félicitations !</div>', unsafe_allow_html=True)
    
    st.balloons()
    
    st.markdown("""
    ### 🎉 Votre système GPS est complet !
    
    Vous avez maintenant :
    - ✅ Une idée validée par le Crash Test D.U.R.
    - ✅ 10 angles stratégiques explorés
    - ✅ Un angle priorisé selon la Matrice de Conviction
    - ✅ Un plan d'action de 7 jours en backcasting
    
    ### 🚀 Prochaines étapes :
    1. Passez à l'action dès aujourd'hui (Jour 1)
    2. Suivez votre plan jour par jour
    3. Ajustez si nécessaire (vous êtes l'Architecte !)
    
    ### 📊 Récapitulatif de votre projet :
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💡 Idée validée")
        st.info(st.session_state.idee_validee)
        
        st.markdown("#### 🎯 Angle choisi")
        if st.session_state.angle_choisi:
            st.success(st.session_state.angle_choisi.get('titre', 'N/A'))
    
    with col2:
        st.markdown("#### 💥 Score Crash Test")
        if st.session_state.crash_test_result:
            total = st.session_state.crash_test_result.get('total', 0)
            verdict = st.session_state.crash_test_result.get('verdict', 'N/A')
            st.metric("Score D.U.R.", f"{total}/30", delta=verdict)
        
        st.markdown("#### 📅 Plan d'action")
        if st.session_state.phase_s_result:
            resultat = st.session_state.phase_s_result.get('resultat_j7', 'N/A')
            st.info(f"Objectif J+7 : {resultat}")
    
    # Téléchargement du plan complet
    st.markdown("---")
    
    plan_complet = {
        'idee_initiale': st.session_state.idee_validee,
        'crash_test': st.session_state.crash_test_result,
        'angles_generes': st.session_state.phase_g_result,
        'angles_selectionnes': st.session_state.angles_selectionnes,
        'priorisation': st.session_state.phase_p_result,
        'angle_choisi': st.session_state.angle_choisi,
        'plan_action': st.session_state.phase_s_result
    }
    
    st.download_button(
        label="📥 Télécharger le plan complet (JSON)",
        data=json.dumps(plan_complet, indent=2, ensure_ascii=False),
        file_name="ia-brainstormer-gps-plan-complet.json",
        mime="application/json",
        use_container_width=True,
        type="primary"
    )
    
    if st.button("🔄 Lancer un nouveau projet", use_container_width=True):
        # Conserver la clé API et le modèle
        api_key_backup = api_key
        model_backup = model_choice
        
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        st.session_state.api_key_backup = api_key_backup
        st.session_state.model_backup = model_backup
        st.rerun()
