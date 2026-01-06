"""
Système GPS IA-BrainStormer
Implémente la méthodologie complète : Crash Test DUR + Génération + Priorisation + Séquençage
"""
# CORRECTIONS ICI : Imports directs (sans 'utils.' ni 'prompts.')
from openai_helper import OpenAIHelper
from system_prompts import (
    SYSTEM_PROMPT_CRASH_TEST,
    SYSTEM_PROMPT_PHASE_G,
    SYSTEM_PROMPT_PHASE_P,
    SYSTEM_PROMPT_PHASE_S
)

class GPSSystem:
    """Classe principale implémentant le système GPS IA-BrainStormer"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """
        Initialise le système GPS
        Args:
            api_key: Clé API OpenAI
            model: Modèle à utiliser
        """
        self.openai_helper = OpenAIHelper(api_key, default_model=model)
        self.model = model
    
    def crash_test_dur(self, idee: str) -> dict:
        """Phase 0 : Crash Test"""
        user_message = f"Analyse cette idée de projet selon la matrice D.U.R. :\n\n{idee}"
        return self.openai_helper.call_gpt(
            system_prompt=SYSTEM_PROMPT_CRASH_TEST,
            user_message=user_message,
            response_format={"type": "json_object"}
        )
    
    def phase_g_generation(self, idee_validee: str) -> dict:
        """Phase G : Génération"""
        user_message = f"Génère 10 angles stratégiques uniques pour cette idée validée :\n\n{idee_validee}"
        return self.openai_helper.call_gpt(
            system_prompt=SYSTEM_PROMPT_PHASE_G,
            user_message=user_message,
            response_format={"type": "json_object"}
        )

    def phase_p_priorisation(self, angles_selectionnes: list) -> dict:
        """Phase P : Priorisation"""
        angles_text = "\n".join([
            f"OPTION {i+1} (ID={a['id']}):\nTitre: {a['titre']}\nCible: {a['cible_precise']}\nOpportunité: {a['opportunite']}\n"
            for i, a in enumerate(angles_selectionnes)
        ])
        
        user_message = f"""Évalue ces 3 options selon la Matrice de Conviction.
        
        OPTIONS À ÉVALUER :
        {angles_text}
        
        RAPPEL PONDÉRATION : Score = (Douleur x 4) + (Unicité x 3) + (Alignement x 3)."""
        
        return self.openai_helper.call_gpt(
            system_prompt=SYSTEM_PROMPT_PHASE_P,
            user_message=user_message,
            response_format={"type": "json_object"}
        )

    def phase_s_sequencage(self, angle_choisi: dict) -> dict:
        """Phase S : Séquençage"""
        user_message = f"""Crée un plan BACKCASTING pour :
        Titre: {angle_choisi['titre']}
        Cible: {angle_choisi['cible_precise']}
        
        Pars de J+7 (Résultat) et remonte à J+1."""
        
        return self.openai_helper.call_gpt(
            system_prompt=SYSTEM_PROMPT_PHASE_S,
            user_message=user_message,
            response_format={"type": "json_object"}
        )
