from openai import OpenAI
import os
import google.generativeai as genai

class EmailAgent:
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "openai").lower()
        
        if self.provider == "gemini":
            self.api_key = os.getenv("GEMINI_API_KEY")
            if self.api_key and not self.api_key.startswith("AIza"):
                self.api_key = None # Invalid key check
            
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.model_client = genai.GenerativeModel('gemini-1.5-flash')
            self.client = "gemini" # Flag for the generator
            
        elif self.provider == "groq":
            self.api_key = os.getenv("GROQ_API_KEY")
            self.base_url = "https://api.groq.com/openai/v1"
            self.model = "llama-3.3-70b-versatile"
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url) if self.api_key else None
        else:
            self.api_key = os.getenv("OPENAI_API_KEY")
            self.model = "gpt-4o"
            self.client = OpenAI(api_key=self.api_key) if self.api_key and self.api_key.startswith("sk-") else None

    def generate_personalized_email(self, recipient_name: str, recipient_role: str, context: str) -> dict:
        """
        Uses an LLM to generate a personalized subject and body for an email.
        """
        if not self.api_key or (self.provider != "gemini" and not self.client):
            return {
                "subject": f"Automated AI Introduction (Demo Mode)",
                "body": f"<p>Hello {recipient_name},</p><p>This is a <b>demo</b> of the automated email since no real API Key for {self.provider.upper()} was provided in the .env file.</p><p>Your Role: {recipient_role}</p>"
            }
        
        prompt = f"""
        You are an expert sales and communication AI agent. 
        Your task is to write a highly professional, engaging, and personalized outreach email.
        
        Recipient Name: {recipient_name}
        Recipient Role/Note: {recipient_role}
        Goal/Context of Email: {context}
        
        Draft the email keeping it concise, polite, and action-oriented. Format the body using basic HTML like <p>, <br>, <strong> if it helps readability.
        
        Please return the result ONLY in the following format:
        SUBJECT: <your generated subject line>
        BODY: <your generated html body>
        """
        
        try:
            if self.provider == "gemini":
                response = self.model_client.generate_content(prompt)
                text = response.text.strip()
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a specialized AI outreach assistant. You provide clean, professional email drafts in HTML format without preamble."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.6
                )
                text = response.choices[0].message.content.strip()
            
            # More robust parsing using regex or refined string splits
            subject = "Personalized Outreach from AI Agent"
            body = text
            
            if "SUBJECT:" in text.upper():
                # Split by BODY: regardless of case
                import re
                parts = re.split(r'BODY:', text, flags=re.IGNORECASE)
                if len(parts) >= 2:
                    subject_line = parts[0].strip()
                    subject = re.sub(r'SUBJECT:', '', subject_line, flags=re.IGNORECASE).strip()
                    body = parts[1].strip()
                else:
                    # Could not find BODY:, try to extract SUBJECT: anyway
                    subject = re.sub(r'SUBJECT:', '', text.split('\n')[0], flags=re.IGNORECASE).strip()
                    body = "\n".join(text.split('\n')[1:]).strip()

            return {
                "subject": subject.replace('"', '').replace("'", ""), # Clean up quotes
                "body": body
            }
            
        except Exception as e:
            print(f"  -> [AI API Error]: {e}")
            return {
                "subject": f"Important Update Regarding {context[:20]}...",
                "body": f"<p>Hello {recipient_name},</p><p>I reached out to discuss {context}, but encountered a slight technical hitch. I'd love to connect regardless!</p><p>Best regards,</p><p>AI Assistant</p>"
            }
