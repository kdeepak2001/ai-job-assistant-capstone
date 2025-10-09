"""Generate a valid Resume PDF file."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

def create_resume_pdf():
    """Create a sample Resume PDF."""
    
    # Output path
    output_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'resume.pdf')
    
    # Create PDF
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    name_style = ParagraphStyle(
        'Name',
        parent=styles['Heading1'],
        fontSize=26,
        textColor='#2575fc',
        spaceAfter=8,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#333333',
        spaceAfter=10,
        spaceBefore=15
    )
    
    # Name and Contact
    name = Paragraph("K Deepak", name_style)
    elements.append(name)
    
    contact = Paragraph(
        "📧 kalavadeepak2002@gmail.com | 📱 +91 9502684256 | 🔗 linkedin.com/in/k-deepak01052002",
        styles['Normal']
    )
    elements.append(contact)
    elements.append(Spacer(1, 20))
    
    # Professional Summary
    summary_heading = Paragraph("PROFESSIONAL SUMMARY", heading_style)
    elements.append(summary_heading)
    
    summary = """
    Recent Electronics and Communication Engineering graduate with strong passion 
    for AI and Data Science. Proficient in Python programming with hands-on experience 
    in machine learning, data analysis, and AI agent development. Completed multiple 
    capstone projects including AI-powered PDF extractors and job application assistants.
    """
    elements.append(Paragraph(summary, styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Education
    edu_heading = Paragraph("EDUCATION", heading_style)
    elements.append(edu_heading)
    
    degree = Paragraph(
        "<b>Bachelor of Engineering - Electronics and Communication</b><br/>University (2020-2024) | CGPA: 5.7",
        styles['Normal']
    )
    elements.append(degree)
    elements.append(Spacer(1, 12))
    
    # Skills
    skills_heading = Paragraph("TECHNICAL SKILLS", heading_style)
    elements.append(skills_heading)
    
    skills = """
    <b>Programming:</b> Python, SQL<br/>
    <b>AI/ML:</b> LangChain, Google Gemini API, OpenAI API, Prompt Engineering<br/>
    <b>Data Analysis:</b> Pandas, NumPy, Data Visualization<br/>
    <b>Tools:</b> Streamlit, Git, GitHub, Jupyter Notebooks, VS Code<br/>
    <b>Web Development:</b> Basic HTML/CSS, API Integration
    """
    elements.append(Paragraph(skills, styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Projects
    projects_heading = Paragraph("PROJECTS", heading_style)
    elements.append(projects_heading)
    
    project1 = """
    <b>AI Job Application Assistant | Capstone Project</b><br/>
    • Built multi-agent system using LangChain and Google Gemini AI for resume optimization<br/>
    • Implemented ATS scoring algorithm achieving 90%+ compatibility<br/>
    • Created automated cover letter generation and interview prep features<br/>
    • Deployed production-ready Streamlit application with modern UI<br/>
    <i>Tech Stack: Python, LangChain, Gemini AI, Streamlit, PDF Processing</i>
    """
    elements.append(Paragraph(project1, styles['Normal']))
    elements.append(Spacer(1, 10))
    
    project2 = """
    <b>AI PDF Extractor with Gemini API</b><br/>
    • Developed intelligent PDF text extraction tool using Google Gemini API<br/>
    • Implemented real-time document analysis and insight generation<br/>
    • Built responsive web interface with glassmorphism design<br/>
    • Achieved 85% reduction in document processing time<br/>
    <i>Tech Stack: Python, Google Gemini, PyPDF2, Streamlit</i>
    """
    elements.append(Paragraph(project2, styles['Normal']))
    elements.append(Spacer(1, 10))
    
    project3 = """
    <b>Financial Data Analysis System</b><br/>
    • Processed and analyzed SEC 10-K documents for Fortune 500 companies<br/>
    • Calculated year-over-year growth metrics for revenue and net income<br/>
    • Built automated data cleaning and validation pipelines<br/>
    • Generated comprehensive financial reports using Pandas<br/>
    <i>Tech Stack: Python, Pandas, Data Analysis, Financial Modeling</i>
    """
    elements.append(Paragraph(project3, styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Certifications
    cert_heading = Paragraph("CERTIFICATIONS", heading_style)
    elements.append(cert_heading)
    
    certs = [
        "BCG GenAI Virtual Experience - Forage",
        "Prompt Engineering Specialization (In Progress)",
        "AI Agent Development Course"
    ]
    
    for cert in certs:
        elements.append(Paragraph(f"• {cert}", styles['Normal']))
        elements.append(Spacer(1, 4))
    
    # Build PDF
    doc.build(elements)
    print(f"✅ Resume PDF created successfully at: {output_path}")
    return output_path

if __name__ == "__main__":
    create_resume_pdf()
