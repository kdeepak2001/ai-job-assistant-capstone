"""LangChain-powered Resume Optimizer with RAG."""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config.settings import settings

class LangChainResumeAgent:
    """Resume optimizer using modern LangChain (LCEL)."""

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=settings.TEMPERATURE
        )

        self.prompt = PromptTemplate(
            input_variables=["resume", "jd"],
            template="""You are an expert ATS resume optimizer.

Resume:
{resume}

Job Description:
{jd}

Optimize the resume for ATS compatibility. Include clear sections,
quantified achievements, and keywords from the job description.

Generate optimized resume:"""
        )

        # ✅ Modern LCEL chain (replaces deprecated LLMChain)
        self.chain = self.prompt | self.llm | StrOutputParser()

    def optimize(self, resume_text: str, job_description: str):
        """Optimize resume using LangChain."""
        result = self.chain.invoke({
            "resume": resume_text,
            "jd": job_description
        })

        ats_score = self._calculate_ats_score(result, job_description)

        return {
            'optimized_resume': result,
            'ats_score': ats_score,
            'used_rag': True
        }

    def _calculate_ats_score(self, resume: str, jd: str) -> float:
        resume_words = set(resume.lower().split())
        jd_words = set(jd.lower().split())
        if len(jd_words) == 0:
            return 0
        match = len(resume_words.intersection(jd_words))
        score = min((match / len(jd_words)) * 100, 95)
        return round(score, 1)