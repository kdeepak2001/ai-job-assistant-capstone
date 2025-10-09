"""Job Description Web Scraper."""
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from config.settings import settings

class JobDescriptionScraper:
    """Scrape and extract job descriptions from URLs."""
    
    @staticmethod
    def scrape_from_url(url: str) -> dict:
        """Scrape job description from URL."""
        try:
            # Fetch webpage
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove scripts and styles
            for script in soup(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()
            
            # Get text
            text = soup.get_text(separator='\n', strip=True)
            
            # Clean up
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            clean_text = '\n'.join(lines)
            
            # Use AI to extract structured JD
            extracted_jd = JobDescriptionScraper._extract_jd_with_ai(clean_text)
            
            return {
                'success': True,
                'job_description': extracted_jd,
                'source_url': url
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'job_description': None
            }
    
    @staticmethod
    def _extract_jd_with_ai(raw_text: str) -> str:
        """Use AI to extract clean job description from messy webpage text."""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(settings.MODEL_NAME)
        
        prompt = f"""Extract and format the job description from this webpage text.

**Raw Webpage Text:**
{raw_text[:8000]}

**Task:**
Extract ONLY the job description information including:
- Job title
- Company name
- Job requirements/qualifications
- Responsibilities
- Skills needed
- Any other relevant job details

Remove navigation, footer, ads, and irrelevant content.

**Output clean, structured job description:**"""
        
        response = model.generate_content(prompt)
        return response.text
