"""Email Follow-up Generator Agent."""
import google.generativeai as genai
from config.settings import settings

class EmailAgent:
    """AI agent for email generation."""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.MODEL_NAME)
    
    def generate_followup(self, company: str, role: str, days_since: int = 7):
        """Generate follow-up email."""
        
        prompt = f"""Write a professional follow-up email.

**Company:** {company}
**Role:** {role}
**Days Since Application:** {days_since}

**Requirements:**
- Professional but warm tone
- 100-150 words
- Reiterate interest
- Add value (mention recent company news if generic)
- Clear call-to-action
- Subject line included

Generate follow-up email:"""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_thank_you(self, company: str, role: str, interviewer_name: str):
        """Generate thank you email after interview."""
        
        prompt = f"""Write a thank you email after interview.

**Company:** {company}
**Role:** {role}
**Interviewer:** {interviewer_name}

**Requirements:**
- Send within 24 hours
- 150-200 words
- Thank them for time
- Reference specific conversation point
- Reiterate fit for role
- Express enthusiasm

Generate thank you email:"""
        
        response = self.model.generate_content(prompt)
        return response.text
