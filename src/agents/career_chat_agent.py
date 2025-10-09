"""AI Career Chat Assistant with conversation memory."""
import google.generativeai as genai
from config.settings import settings

class CareerChatAgent:
    """AI-powered career advisor chatbot."""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.MODEL_NAME)
        self.conversation_history = []
    
    def chat(self, user_message: str, resume_context: str = None) -> str:
        """Chat with career advisor."""
        
        # Build context
        context = "You are an expert career advisor helping job seekers.\n\n"
        
        if resume_context:
            context += f"**User's Background:**\n{resume_context}\n\n"
        
        # Add conversation history
        if self.conversation_history:
            context += "**Previous Conversation:**\n"
            for msg in self.conversation_history[-6:]:  # Last 3 exchanges
                context += f"{msg}\n"
        
        context += f"\n**User Question:** {user_message}\n\n"
        context += """**Instructions:**
- Provide actionable career advice
- Be encouraging and supportive
- Give specific examples and resources
- Keep response under 200 words
- Use bullet points for clarity

**Your Response:**"""
        
        response = self.model.generate_content(context)
        answer = response.text
        
        # Store in history
        self.conversation_history.append(f"User: {user_message}")
        self.conversation_history.append(f"Assistant: {answer}")
        
        return answer
    
    def reset_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []
