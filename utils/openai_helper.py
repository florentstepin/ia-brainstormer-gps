"""
Module de gestion des appels à l'API OpenAI
"""
import json
from openai import OpenAI


class OpenAIHelper:
    """Classe pour gérer les appels à l'API OpenAI avec gestion d'erreurs"""
    
    def __init__(self, api_key: str, default_model: str = "gpt-4o"):
        """
        Initialise le client OpenAI
        
        Args:
            api_key: Clé API OpenAI
            default_model: Modèle par défaut à utiliser
        """
        # Correction : Initialisation simplifiée sans paramètres supplémentaires
        self.client = OpenAI(api_key=api_key)
        self.default_model = default_model
    
    def call_gpt(self, system_prompt: str, user_message: str, model: str = None, response_format: dict = None) -> dict:
        """
        Appelle l'API OpenAI avec un prompt système et un message utilisateur
        
        Args:
            system_prompt: Le prompt système définissant le rôle de l'IA
            user_message: Le message de l'utilisateur
            model: Le modèle à utiliser (si None, utilise default_model)
            response_format: Format de réponse attendu (ex: {"type": "json_object"})
        
        Returns:
            dict: La réponse parsée en JSON
        """
        # Utiliser le modèle par défaut si non spécifié
        if model is None:
            model = self.default_model
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # Paramètres de l'appel
            call_params = {
                "model": model,
                "messages": messages,
                "temperature": 0.7
            }
            
            # Ajouter le format de réponse si spécifié
            if response_format:
                call_params["response_format"] = response_format
            
            response = self.client.chat.completions.create(**call_params)
            
            content = response.choices[0].message.content
            
            # Tenter de parser en JSON
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Si ce n'est pas du JSON, retourner le texte brut
                return {"raw_response": content}
                
        except Exception as e:
            return {
                "error": True,
                "message": f"Erreur lors de l'appel à l'API : {str(e)}"
            }
