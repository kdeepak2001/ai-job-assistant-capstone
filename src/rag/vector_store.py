"""RAG Vector Store for Resume Database."""
import chromadb
from chromadb.config import Settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from config.settings import settings
from typing import List, Dict

class ResumeVectorStore:
    """Vector database for storing and retrieving resume information."""
    
    def __init__(self):
        """Initialize vector store with ChromaDB."""
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=settings.GEMINI_API_KEY
        )
        
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./data/chroma_db"
        ))
        
        self.collection_name = "resumes"
        self.vectorstore = None
        self._initialize_vectorstore()
    
    def _initialize_vectorstore(self):
        """Initialize or load existing vector store."""
        try:
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory="./data/chroma_db"
            )
        except:
            self.vectorstore = Chroma.from_documents(
                documents=[],
                embedding=self.embeddings,
                collection_name=self.collection_name,
                persist_directory="./data/chroma_db"
            )
    
    def add_resume(self, resume_text: str, metadata: Dict):
        """Add resume to vector database."""
        # Split resume into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        
        chunks = text_splitter.create_documents(
            [resume_text],
            metadatas=[metadata]
        )
        
        # Add to vector store
        self.vectorstore.add_documents(chunks)
        self.vectorstore.persist()
    
    def search_similar_resumes(self, query: str, k: int = 3) -> List[Dict]:
        """Search for similar resume sections."""
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        
        return [
            {
                'content': doc.page_content,
                'metadata': doc.metadata,
                'score': score
            }
            for doc, score in results
        ]
    
    def get_relevant_context(self, job_description: str, k: int = 5) -> str:
        """Get relevant resume context for a job description."""
        results = self.search_similar_resumes(job_description, k=k)
        
        context = "\n\n---\n\n".join([
            f"**Similar Resume Section:**\n{r['content']}"
            for r in results
        ])
        
        return context
