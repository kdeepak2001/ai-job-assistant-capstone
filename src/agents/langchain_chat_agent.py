"""LangChain Chat Agent with Memory and RAG."""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from config.settings import settings
from src.rag.vector_store import ResumeVectorStore

class LangChainChatAgent:
    """Conversational AI career advisor with memory and context."""
    
    def __init__(self):
        """Initialize chat agent with memory."""
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.7
        )
        
        self.vector_store = ResumeVectorStore()
        
        # Conversation memory (remembers last 5 exchanges)
        self.memory = ConversationBufferWindowMemory(
            k=5,
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Create retrieval chain
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.vectorstore.as_retriever(
                search_kwargs={"k": 3}
            ),
            memory=self.memory,
            return_source_documents=True
        )
    
    def chat(self, user_question: str) -> Dict:
        """Chat with context awareness."""
        result = self.qa_chain({"question": user_question})
        
        return {
            'answer': result['answer'],
            'sources': [doc.page_content for doc in result['source_documents']]
        }
    
    def reset_memory(self):
        """Clear conversation history."""
        self.memory.clear()
