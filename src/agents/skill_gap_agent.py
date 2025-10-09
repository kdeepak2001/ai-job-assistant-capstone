"""Skill Gap Analysis Agent - Identifies missing skills."""
import google.generativeai as genai
from config.settings import settings

class SkillGapAgent:
    """AI agent for skill gap analysis."""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.MODEL_NAME)
    
    def analyze(self, resume_text: str, job_description: str):
        """Analyze skill gaps between resume and JD."""
        
        prompt = f"""You are an expert career coach analyzing skill gaps.

**Candidate Resume:**
{resume_text}

**Job Description:**
{job_description}

**Task:** Perform comprehensive skill gap analysis.

**Output Format:**

## ✅ MATCHING SKILLS (You Already Have)
• [Skill 1] - [How it appears in your resume]
• [Skill 2] - [How it appears in your resume]
• [Skill 3] - [How it appears in your resume]

## ⚠️ SKILL GAPS (Need to Learn/Highlight)
• [Skill 1] - [Required in JD, not in resume]
• [Skill 2] - [Required in JD, not in resume]
• [Skill 3] - [Required in JD, not in resume]

## 🎯 PARTIALLY MATCHING SKILLS (Need Improvement)
• [Skill 1] - [You have basic knowledge, JD wants advanced]
• [Skill 2] - [Similar but different tool/technology]

## 📚 LEARNING RECOMMENDATIONS
1. **[Skill 1]**: Learn via [Free resource/course name]
2. **[Skill 2]**: Learn via [Free resource/course name]
3. **[Skill 3]**: Learn via [Free resource/course name]

## ⏱️ ESTIMATED TIME TO CLOSE GAPS
- **High Priority Skills**: [X weeks]
- **Medium Priority Skills**: [Y weeks]
- **Total Time**: [Z weeks]

## 💡 ACTION PLAN
1. [Immediate action]
2. [Short-term action]
3. [Long-term action]

Generate detailed analysis:"""
        
        response = self.model.generate_content(prompt)
        return response.text
