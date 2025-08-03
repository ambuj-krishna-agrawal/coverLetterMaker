#!/usr/bin/env python3

import os
from google import genai

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-flash"
        
    def generate_text(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate text using Gemini API"""
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()
                
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            raise Exception(f"Gemini API call failed: {str(e)}")
    
    
    def is_configured(self) -> bool:
        """Check if LLM is properly configured"""
        return bool(self.api_key)