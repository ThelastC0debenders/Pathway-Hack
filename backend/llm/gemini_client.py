import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("[LLM] ❌ ERROR: GOOGLE_API_KEY not found!")
            raise ValueError("Missing GOOGLE_API_KEY")

        # Configure the API key
        genai.configure(api_key=api_key)
        self.model_id = "gemini-2.0-flash-exp"  # Updated to valid model
        
        print(f"[LLM] 🤖 Gemini Client initialized using {self.model_id}")
    
    # ✅ FIX: Proper indentation - must be inside the class!
    def generate(self, prompt: str, system_instruction: str = None):
        try:
            # Create generation config
            generation_config = {
                "temperature": 0.3,
            }
            
            model = genai.GenerativeModel(
                model_name=self.model_id,
                system_instruction=system_instruction
            )
            
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            
            # Extract text from response
            if hasattr(response, 'text'):
                return response.text
            elif hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content'):
                    if hasattr(candidate.content, 'parts'):
                        if candidate.content.parts:
                            text = candidate.content.parts[0].text
                            return text
            
            print("[DEBUG] Failed to extract text from response")
            return "⚠️ Could not extract text from response"
            
        except Exception as e:
            print(f"[LLM ERROR] {e}")
            import traceback
            traceback.print_exc()
            return f"Error: {str(e)}"