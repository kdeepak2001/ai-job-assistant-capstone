"""
Production-grade PDF parser with multiple extraction methods and fallbacks.
Handles corrupted PDFs, scanned images, and various PDF formats.
"""

import io
import tempfile
from pathlib import Path
from typing import Optional, Dict

# Multiple PDF libraries for fallback
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

try:
    from pdfminer.high_level import extract_text as pdfminer_extract
    HAS_PDFMINER = True
except ImportError:
    HAS_PDFMINER = False


class PDFParser:
    """Advanced PDF parsing with multiple extraction strategies."""
    
    MIN_TEXT_LENGTH = 50
    
    @staticmethod
    def extract_text(uploaded_file) -> str:
        """
        Extract text from PDF using multiple methods with intelligent fallback.
        
        Priority:
        1. pdfplumber (best for most PDFs)
        2. PyPDF2 (faster, works with simple PDFs)
        3. pdfminer (works with complex PDFs)
        4. Temp file method (last resort)
        """
        
        # Reset file pointer
        uploaded_file.seek(0)
        
        # Try Method 1: pdfplumber with BytesIO
        if HAS_PDFPLUMBER:
            result = PDFParser._extract_with_pdfplumber_bytes(uploaded_file)
            if PDFParser.validate_pdf(result):
                return result
        
        # Reset for next method
        uploaded_file.seek(0)
        
        # Try Method 2: PyPDF2 with BytesIO
        if HAS_PYPDF2:
            result = PDFParser._extract_with_pypdf2(uploaded_file)
            if PDFParser.validate_pdf(result):
                return result
        
        # Reset for next method
        uploaded_file.seek(0)
        
        # Try Method 3: Save to temp file and process
        result = PDFParser._extract_with_tempfile(uploaded_file)
        if PDFParser.validate_pdf(result):
            return result
        
        return "Error: Could not extract text from PDF. The file may be corrupted, password-protected, or scanned image-based."
    
    @staticmethod
    def _extract_with_pdfplumber_bytes(uploaded_file) -> str:
        """Extract using pdfplumber with BytesIO."""
        try:
            pdf_bytes = uploaded_file.read()
            pdf_file = io.BytesIO(pdf_bytes)
            
            text = ""
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            uploaded_file.seek(0)
            return text.strip()
        except Exception as e:
            print(f"pdfplumber extraction failed: {e}")
            return ""
    
    @staticmethod
    def _extract_with_pypdf2(uploaded_file) -> str:
        """Extract using PyPDF2."""
        try:
            pdf_bytes = uploaded_file.read()
            pdf_file = io.BytesIO(pdf_bytes)
            
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            uploaded_file.seek(0)
            return text.strip()
        except Exception as e:
            print(f"PyPDF2 extraction failed: {e}")
            return ""
    
    @staticmethod
    def _extract_with_tempfile(uploaded_file) -> str:
        """Extract by saving to temporary file (last resort)."""
        try:
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = Path(tmp.name)
            
            # Try pdfplumber on temp file
            if HAS_PDFPLUMBER:
                try:
                    text = ""
                    with pdfplumber.open(tmp_path) as pdf:
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                    
                    tmp_path.unlink()  # Delete temp file
                    uploaded_file.seek(0)
                    return text.strip()
                except:
                    pass
            
            # Try PyPDF2 on temp file
            if HAS_PYPDF2:
                try:
                    with open(tmp_path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        text = ""
                        for page in reader.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                    
                    tmp_path.unlink()
                    uploaded_file.seek(0)
                    return text.strip()
                except:
                    pass
            
            # Try pdfminer on temp file
            if HAS_PDFMINER:
                try:
                    text = pdfminer_extract(str(tmp_path))
                    tmp_path.unlink()
                    uploaded_file.seek(0)
                    return text.strip()
                except:
                    pass
            
            # Cleanup
            if tmp_path.exists():
                tmp_path.unlink()
            
            uploaded_file.seek(0)
            return ""
            
        except Exception as e:
            print(f"Temp file extraction failed: {e}")
            uploaded_file.seek(0)
            return ""
    
    @staticmethod
    def validate_pdf(text: str) -> bool:
        """Validate if PDF extraction was successful."""
        if not text or text.startswith("Error"):
            return False
        
        # Check if text is meaningful
        if len(text.strip()) < PDFParser.MIN_TEXT_LENGTH:
            return False
        
        # Check if text has actual words (not just special characters)
        words = text.split()
        if len(words) < 10:
            return False
        
        return True
    
    @staticmethod
    def get_pdf_info(uploaded_file) -> Dict:
        """Get PDF metadata and basic information."""
        try:
            uploaded_file.seek(0)
            pdf_bytes = uploaded_file.read()
            pdf_file = io.BytesIO(pdf_bytes)
            
            if HAS_PYPDF2:
                reader = PyPDF2.PdfReader(pdf_file)
                info = {
                    'num_pages': len(reader.pages),
                    'encrypted': reader.is_encrypted,
                    'metadata': reader.metadata if reader.metadata else {}
                }
                uploaded_file.seek(0)
                return info
            
            uploaded_file.seek(0)
            return {'num_pages': 0, 'encrypted': False, 'metadata': {}}
            
        except:
            uploaded_file.seek(0)
            return {'num_pages': 0, 'encrypted': False, 'metadata': {}}
