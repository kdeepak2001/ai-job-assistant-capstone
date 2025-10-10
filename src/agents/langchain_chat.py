"""LangChain Chat Agent."""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from config.settings import settings

class LangChainChatAgent:
    """Career advisor with memory."""
    
    def __init__(self):
        """Initialize chat agent."""
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.7
        )
        
        self.memory = ConversationBufferMemory()
        
        self.chain = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=False
        )
    
    def chat(self, user_message: str, resume_context: str = None) -> str:
        """Chat with memory."""
        response = self.chain.predict(input=user_message)
        return response
    
    def reset_conversation(self):
        """Clear memory."""
        self.memory.clear()
