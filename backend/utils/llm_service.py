
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMService:
    def __init__(self):
        self.providers = []
        self._initialize_providers()

    def _initialize_providers(self):
        # 1. OpenAI (Priority 1)
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and len(openai_key) > 10:
            try:
                from openai import OpenAI
                self.providers.append({
                    "name": "openai",
                    "client": OpenAI(api_key=openai_key),
                    "model": "gpt-4o"
                })
                print("Registered LLM Provider: OpenAI")
            except Exception as e:
                print(f"Failed to init OpenAI: {e}")

        # 2. Groq (Priority 2)
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key and len(groq_key) > 10:
            try:
                from groq import Groq
                self.providers.append({
                    "name": "groq",
                    "client": Groq(api_key=groq_key),
                    "model": "llama-3.3-70b-versatile"
                })
                print("Registered LLM Provider: Groq")
            except Exception as e:
                print(f"Failed to init Groq: {e}")

        # 3. Gemini (Priority 3)
        gemini_key = os.getenv("GOOGLE_API_KEY")
        if gemini_key and len(gemini_key) > 10:
            try:
                genai.configure(api_key=gemini_key)
                # Using gemini-1.5-flash (current recommended model)
                self.providers.append({
                    "name": "gemini",
                    "client": genai.GenerativeModel('gemini-1.5-flash'),
                    "model": "gemini-1.5-flash"
                })
                print("Registered LLM Provider: Gemini")
            except Exception as e:
                print(f"Failed to init Gemini: {e}")

        if not self.providers:
            print("CRITICAL WARNING: No LLM providers could be initialized. Check .env keys.")

    def generate_response(self, prompt):
        if not self.providers:
            return "System Error: No valid LLM API keys found (OpenAI/Groq/Gemini). Please check .env."
            
        errors = []
        
        # Try each provider in order
        for provider in self.providers:
            try:
                print(f"Attempting generation with {provider['name']}...")
                if provider['name'] == "gemini":
                    response = provider['client'].generate_content(prompt)
                    return response.text
                
                elif provider['name'] in ["openai", "groq"]:
                    response = provider['client'].chat.completions.create(
                        model=provider['model'],
                        messages=[{"role": "user", "content": prompt}]
                    )
                    return response.choices[0].message.content
                    
            except Exception as e:
                error_msg = f"{provider['name']} failed: {str(e)}"
                print(error_msg)
                errors.append(error_msg)
                continue # Try next provider
        
        return "All LLM providers failed.\n" + "\n".join(errors)

# Singleton instance
llm_service = LLMService()
