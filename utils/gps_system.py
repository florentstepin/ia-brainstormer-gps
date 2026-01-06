"""
Système GPS IA-BrainStormer
Implémente la méthodologie complète : Crash Test DUR + Génération + Priorisation + Séquençage
"""
from utils.openai_helper import OpenAIHelper
from prompts.system_prompts import (
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
            model: Modèle à utiliser (gpt-4o, gpt-4-turbo, gpt-3.5-turbo, etc.)
        """
        self.openai_helper = OpenAIHelper(api_key, default_model=model)
        self.model = model
    
    def crash_test_dur(self, idee: str) -> dict:
        """
        Phase 0 : Crash Test avec matrice D.U.R.
        Identifie le maillon faible et propose un conseil spécifique
        
        Args:
            idee: L'idée de projet à tester
        
        Returns:
            dict: Résultat du crash test avec scores D.U.R., verdict et conseil
        """
        user_message = f"Analyse cette idée de projet selon la matrice D.U.R. :\n\n{idee}"
        
        result = self.openai_helper.call_gpt(
            system_prompt=SYSTEM_PROMPT_CRASH_TEST,
            user_message=user_message,
            response_format={"type": "json_object"}
        )
        
        # Identifier le maillon faible
        if "error" not in result:
            scores = {
                "Douloureux": result.get("score_D", 0),
                "Urgent": result.get("score_U", 0),
                "Reconnu": result.get("score_R", 0)
            }
            maillon_faible = min(scores, key=scores.get)
            result["maillon_faible"] = maillon_faible
            result["score_maillon_faible"] = scores[maillon_faible]
        
        return result
    
    def phase_g_generation(self, idee_validee: str) -> dict:
        """
        Phase G : Génération de 10 angles avec l'Explorateur de Perspective
        
        Args:
            idee_validee: L'idée validée après le crash test (potentiellement modifiée par l'utilisateur)
        
        Returns:
            dict: Liste de 10 angles avec titre, cible précise et opportunité
        """
        user_message = f"Génère 10 angles stratégiques radicalement différents pour cette idée :\n\n{idee_validee}"
        
        result = self.openai_helper.call_gpt(
            system_prompt=SYSTEM_PROMPT_PHASE_G,
            user_message=user_message,
            response_format={"type": "json_object"}
        )
        
        return result
    
    def phase_p_priorisation(self, angles_selectionnes: list) -> dict:
        """
        Phase P : Priorisation avec la Matrice de Conviction
        Pondération : Douleur Client (40%) + Unicité (30%) + Alignement (30%)
        
        Args:
            angles_selectionnes: Liste de 3 angles sélectionnés par l'utilisateur
        
        Returns:
            dict: Évaluation comparative avec scores pondérés et recommandation
        """
        # Formater les angles pour le prompt
        angles_text = "\n\n".join([
            f"Option {i+1}:\nTitre: {angle['titre']}\nCible: {angle['cible_precise']}\nOpportunité: {angle['opportunite']}"
            for i, angle in enumerate(angles_selectionnes)
        ])
        
        user_message = f"""Évalue ces 3 options selon la Matrice de Conviction (Douleur 40% + Unicité 30% + Alignement 30%) :

{angles_text}

IMPORTANT : Calcule le score total pondéré ainsi :
Score Total = (Score Douleur × 4) + (Score Unicité × 3) + (Score Alignement × 3)
Le score maximum est donc 100 points."""
        
        result = self.openai_helper.call_gpt(
            system_prompt=SYSTEM_PROMPT_PHASE_P,
            user_message=user_message,
            response_format={"type": "json_object"}
        )
        
        return result
    
    def phase_s_sequencage(self, angle_choisi: dict) -> dict:
        """
        Phase S : Séquençage avec méthode Backcasting (de J+7 à J+1)
        
        Args:
            angle_choisi: L'angle sélectionné après la phase P (potentiellement modifié par l'utilisateur)
        
        Returns:
            dict: Plan d'action de 7 jours en backcasting
        """
        user_message = f"""Crée un plan d'action de 7 jours en BACKCASTING pour ce projet :

Titre: {angle_choisi['titre']}
Cible: {angle_choisi['cible_precise']}
Opportunité: {angle_choisi['opportunite']}

Commence par définir le résultat final à J+7, puis remonte jour par jour jusqu'à J+1."""
        
        result = self.openai_helper.call_gpt(
            system_prompt=SYSTEM_PROMPT_PHASE_S,
            user_message=user_message,
            response_format={"type": "json_object"}
        )
        
        return result
