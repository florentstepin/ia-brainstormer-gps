"""
Module de gestion des appels à l'API OpenAI
"""
import json
from openai import OpenAI

class OpenAIHelper:
    """Classe pour gérer les appels à l'API OpenAI avec gestion d'erreurs"""
    
    def __init__(self, api_key: str, default_model: str = "gpt-4o"):
        self.client = OpenAI(api_key=api_key)
        self.default_model = default_model
    
    def call_gpt(self, system_prompt: str, user_message: str, model: str = None, response_format: dict = None) -> dict:
        if model is None:
            model = self.default_model
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            call_params = {
                "model": model,
                "messages": messages,
                "temperature": 0.7
            }
            
            if response_format:
                call_params["response_format"] = response_format
            
            response = self.client.chat.completions.create(**call_params)
            content = response.choices[0].message.content
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {"raw_response": content, "error": "JSON parsing failed"}
                
        except Exception as e:
            return {
                "error": True,
                "message": f"Erreur API : {str(e)}"
            }
