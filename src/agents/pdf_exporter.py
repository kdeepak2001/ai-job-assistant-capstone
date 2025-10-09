"""Export optimized resume to styled PDF with multiple templates."""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime
import io

class PDFExporter:
    """Export resume to PDF with professional templates."""
    
    TEMPLATES = {
        'modern': {
            'name': 'Modern Blue',
            'primary_color': colors.HexColor('#2575fc'),
            'secondary_color': colors.HexColor('#6a11cb'),
            'accent_color': colors.HexColor('#764ba2')
        },
        'professional': {
            'name': 'Professional Black',
            'primary_color': colors.HexColor('#1a1a1a'),
            'secondary_color': colors.HexColor('#333333'),
            'accent_color': colors.HexColor('#555555')
        },
        'creative': {
            'name': 'Creative Purple',
            'primary_color': colors.HexColor('#667eea'),
            'secondary_color': colors.HexColor('#764ba2'),
            'accent_color': colors.HexColor('#f093fb')
        },
        'minimal': {
            'name': 'Minimal Grey',
            'primary_color': colors.HexColor('#2d3748'),
            'secondary_color': colors.HexColor('#4a5568'),
            'accent_color': colors.HexColor('#718096')
        }
    }
    
    @classmethod
    def export(cls, resume_text: str, template: str = 'modern', 
               candidate_name: str = "Candidate", company_name: str = "Company") -> bytes:
        """Export resume to PDF with chosen template."""
        
        # Create PDF in memory
        buffer = io.BytesIO()
        
        # Get template colors
        theme = cls.TEMPLATES.get(template, cls.TEMPLATES['modern'])
        
        # Create document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.5*inch
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles based on template
        name_style = ParagraphStyle(
            'CustomName',
            parent=styles['Heading1'],
            fontSize=26,
            textColor=theme['primary_color'],
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=theme['secondary_color'],
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=theme['accent_color'],
            borderPadding=5
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.black,
            alignment=TA_JUSTIFY,
            spaceAfter=6
        )
        
        # Header with colored bar
        header_table = Table([['']], colWidths=[7*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), theme['primary_color']),
            ('HEIGHT', (0, 0), (-1, -1), 0.3*inch)
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 10))
        
        # Candidate Name
        name = Paragraph(candidate_name.upper(), name_style)
        elements.append(name)
        
        # Target company
        target = Paragraph(
            f"<i>Resume optimized for: {company_name}</i>",
            styles['Normal']
        )
        elements.append(target)
        elements.append(Spacer(1, 15))
        
        # Process resume text by sections
        sections = resume_text.split('##')
        
        for section in sections:
            if not section.strip():
                continue
            
            lines = section.strip().split('\n')
            if not lines:
                continue
            
            # Section heading
            section_title = lines[0].strip()
            if section_title:
                heading = Paragraph(section_title, heading_style)
                elements.append(heading)
            
            # Section content
            content = '\n'.join(lines[1:]).strip()
            if content:
                # Convert markdown bullets to proper formatting
                content_lines = content.split('\n')
                for line in content_lines:
                    if line.strip():
                        # Handle bullet points
                        if line.strip().startswith('•') or line.strip().startswith('-'):
                            line = line.strip().lstrip('•-').strip()
                            para = Paragraph(f"• {line}", body_style)
                        elif line.strip().startswith('**'):
                            # Bold text
                            line = line.replace('**', '<b>').replace('**', '</b>')
                            para = Paragraph(line, body_style)
                        else:
                            para = Paragraph(line, body_style)
                        
                        elements.append(para)
                        elements.append(Spacer(1, 3))
            
            elements.append(Spacer(1, 8))
        
        # Footer
        footer_text = f"Generated by AI Job Assistant | {datetime.now().strftime('%B %Y')}"
        footer = Paragraph(
            f"<font size=8 color='gray'><i>{footer_text}</i></font>",
            styles['Normal']
        )
        elements.append(Spacer(1, 20))
        elements.append(footer)
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    @classmethod
    def get_template_names(cls):
        """Get list of available template names."""
        return {key: value['name'] for key, value in cls.TEMPLATES.items()}
