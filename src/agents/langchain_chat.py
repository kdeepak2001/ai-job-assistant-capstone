"""LangChain Chat Agent with Memory."""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from config.settings import settings

class LangChainChatAgent:
    """Career advisor with conversation memory using modern LangChain."""

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.7
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert career advisor. Give concise, actionable advice."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])

        self.store = {}
        chain = self.prompt | self.llm

        # ✅ Modern memory management
        self.chain_with_history = RunnableWithMessageHistory(
            chain,
            self._get_session_history,
            input_messages_key="input",
            history_messages_key="history"
        )

    def _get_session_history(self, session_id: str):
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
        return self.store[session_id]

    def chat(self, user_message: str, resume_context: str = None) -> str:
        message = user_message
        if resume_context:
            message = f"Context about me: {resume_context[:500]}\n\nQuestion: {user_message}"

        response = self.chain_with_history.invoke(
            {"input": message},
            config={"configurable": {"session_id": "default"}}
        )
        return response.content

    def reset_conversation(self):
        self.store.clear()