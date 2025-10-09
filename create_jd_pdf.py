"""Generate a valid Job Description PDF file."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

def create_jd_pdf():
    """Create a sample Job Description PDF."""
    
    # Output path
    output_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'jd.pdf')
    
    # Create PDF
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#2575fc',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#333333',
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Job Description Content
    title = Paragraph("Data Analyst Position", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    company = Paragraph("<b>Company:</b> Google Inc.", styles['Normal'])
    elements.append(company)
    elements.append(Spacer(1, 6))
    
    location = Paragraph("<b>Location:</b> Bangalore, India", styles['Normal'])
    elements.append(location)
    elements.append(Spacer(1, 6))
    
    job_type = Paragraph("<b>Job Type:</b> Full-time", styles['Normal'])
    elements.append(job_type)
    elements.append(Spacer(1, 20))
    
    # Job Description Section
    jd_heading = Paragraph("Job Description", heading_style)
    elements.append(jd_heading)
    
    jd_text = """
    We are seeking a talented Data Analyst to join our dynamic team. 
    The ideal candidate will have strong analytical skills and the ability 
    to translate data into actionable insights that drive business decisions.
    """
    elements.append(Paragraph(jd_text, styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Requirements Section
    req_heading = Paragraph("Requirements", heading_style)
    elements.append(req_heading)
    
    requirements = [
        "Bachelor's degree in Computer Science, Statistics, Mathematics, or related field",
        "2+ years of experience in data analysis or related role",
        "Strong proficiency in Python and SQL",
        "Experience with data visualization tools (Power BI, Tableau, or similar)",
        "Excellent analytical and problem-solving skills",
        "Strong communication skills to present findings to stakeholders",
        "Experience with Excel and statistical analysis",
        "Knowledge of machine learning concepts is a plus"
    ]
    
    for req in requirements:
        bullet = Paragraph(f"• {req}", styles['Normal'])
        elements.append(bullet)
        elements.append(Spacer(1, 6))
    
    elements.append(Spacer(1, 12))
    
    # Responsibilities Section
    resp_heading = Paragraph("Key Responsibilities", heading_style)
    elements.append(resp_heading)
    
    responsibilities = [
        "Analyze large datasets to identify trends, patterns, and insights",
        "Create comprehensive dashboards and reports for stakeholders",
        "Collaborate with cross-functional teams to understand business needs",
        "Develop data-driven recommendations to improve business processes",
        "Design and maintain automated reporting systems",
        "Perform statistical analysis and predictive modeling",
        "Ensure data quality and integrity across systems",
        "Present findings and insights to management teams"
    ]
    
    for resp in responsibilities:
        bullet = Paragraph(f"• {resp}", styles['Normal'])
        elements.append(bullet)
        elements.append(Spacer(1, 6))
    
    elements.append(Spacer(1, 12))
    
    # Preferred Skills Section
    pref_heading = Paragraph("Preferred Skills", heading_style)
    elements.append(pref_heading)
    
    preferred = [
        "Experience with cloud platforms (AWS, GCP, Azure)",
        "Knowledge of ETL pipeline development",
        "Familiarity with Spark, Hadoop, or other big data technologies",
        "Experience with A/B testing and experimental design",
        "Understanding of business intelligence concepts"
    ]
    
    for pref in preferred:
        bullet = Paragraph(f"• {pref}", styles['Normal'])
        elements.append(bullet)
        elements.append(Spacer(1, 6))
    
    # Build PDF
    doc.build(elements)
    print(f"✅ PDF created successfully at: {output_path}")
    return output_path

if __name__ == "__main__":
    create_jd_pdf()
