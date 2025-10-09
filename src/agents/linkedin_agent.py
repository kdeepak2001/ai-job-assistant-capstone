"""LinkedIn Profile Optimization Agent."""
import google.generativeai as genai
from config.settings import settings

class LinkedInAgent:
    """AI agent for LinkedIn profile optimization."""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.MODEL_NAME)
    
    def generate_about_section(self, resume_text: str, target_role: str):
        """Generate LinkedIn About section."""
        
        prompt = f"""Write a compelling LinkedIn "About" section.

**Resume:** {resume_text}

**Target Role:** {target_role}

**Requirements:**
- 150-200 words
- First-person narrative
- Hook in first line
- Highlight unique value proposition
- Include 3-4 key achievements with metrics
- End with call-to-action
- SEO-optimized with industry keywords

Generate LinkedIn About section:"""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_headline(self, resume_text: str, target_role: str):
        """Generate LinkedIn headline."""
        
        prompt = f"""Create a powerful LinkedIn headline (max 220 characters).

**Resume:** {resume_text}
**Target Role:** {target_role}

Format: [Current Role] | [Key Skill 1] | [Key Skill 2] | [Unique Value]

Generate 3 headline options:"""
        
        response = self.model.generate_content(prompt)
        return response.text
