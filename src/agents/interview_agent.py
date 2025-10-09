"""Interview preparation agent."""
import google.generativeai as genai
from config.settings import settings

class InterviewAgent:
    """AI agent for interview preparation."""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.MODEL_NAME)
    
    def generate(self, resume_text: str, job_description: str, role: str):
        """Generate interview questions and answers."""
        
        prompt = f"""Generate 10 interview questions with STAR-format answers.

**Resume:** {resume_text}

**Job Description:** {job_description}

**Role:** {role}

**Categories:**
- 4 Technical questions
- 4 Behavioral questions
- 2 Situational questions

**Format for each:**

### Question X: [Category]
**Q:** [Question]

**Answer (STAR):**
- **Situation:** [Context]
- **Task:** [Challenge]
- **Action:** [Steps taken]
- **Result:** [Outcome with metrics]

Generate all 10 questions:"""
        
        response = self.model.generate_content(prompt)
        return response.text
