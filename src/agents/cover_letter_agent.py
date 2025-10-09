"""Cover letter generation agent."""
import google.generativeai as genai
from config.settings import settings

class CoverLetterAgent:
    """AI agent for cover letter generation."""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.MODEL_NAME)
    
    def generate(self, resume_text: str, job_description: str, company: str, role: str):
        """Generate tailored cover letter."""
        
        prompt = f"""Write a professional cover letter (300-400 words).

**Resume:** {resume_text}

**Job Description:** {job_description}

**Company:** {company}
**Role:** {role}

**Structure:**
1. Opening: Express genuine interest in role and company
2. Body: Connect top 3 skills to JD requirements with specific achievements
3. Closing: Strong call-to-action for interview

**Tone:** Professional, confident, enthusiastic

Generate the cover letter:"""
        
        response = self.model.generate_content(prompt)
        return response.text
