"""LangChain-powered Resume Optimizer with RAG."""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.chains import LLMChain
from config.settings import settings
from src.rag.vector_store import ResumeVectorStore

class LangChainResumeOptimizer:
    """Advanced resume optimizer using LangChain + RAG."""
    
    def __init__(self):
        """Initialize LangChain components."""
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=settings.TEMPERATURE
        )
        
        self.vector_store = ResumeVectorStore()
        
        # Define output schema
        self.response_schemas = [
            ResponseSchema(name="optimized_resume", description="The optimized resume text"),
            ResponseSchema(name="ats_score", description="ATS compatibility score (0-100)"),
            ResponseSchema(name="improvements", description="List of improvements made"),
            ResponseSchema(name="keywords_added", description="List of keywords added")
        ]
        
        self.output_parser = StructuredOutputParser.from_response_schemas(
            self.response_schemas
        )
    
    def optimize(self, resume_text: str, job_description: str):
        """Optimize resume using RAG context."""
        
        # Get similar resume examples from vector DB
        similar_context = self.vector_store.get_relevant_context(job_description)
        
        # Create prompt template
        prompt_template = ChatPromptTemplate.from_template(
            """You are an expert ATS resume optimizer with access to successful resume examples.

**Current Resume:**
{resume_text}

**Target Job Description:**
{job_description}

**Similar Successful Resume Examples:**
{similar_context}

**Task:**
Optimize the resume to maximize ATS score by:
1. Analyzing successful patterns from similar resumes
2. Matching keywords from job description
3. Quantifying achievements with metrics
4. Using ATS-friendly formatting
5. Highlighting relevant skills

{format_instructions}

Generate the optimized resume:"""
        )
        
        # Create chain
        chain = LLMChain(
            llm=self.llm,
            prompt=prompt_template,
            output_parser=self.output_parser
        )
        
        # Run chain
        result = chain.run(
            resume_text=resume_text,
            job_description=job_description,
            similar_context=similar_context,
            format_instructions=self.output_parser.get_format_instructions()
        )
        
        return result
