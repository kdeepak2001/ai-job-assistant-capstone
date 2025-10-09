"""Export optimized resume to styled PDF with multiple templates."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime
import io
import re

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
    
    @staticmethod
    def clean_html(text):
        """Clean and fix malformed HTML tags."""
        if not text:
            return ""
        
        # Fix unclosed bold tags
        text = re.sub(r'<b>([^<]*)<b>', r'<b>\1</b>', text)
        
        # Fix double bold tags
        text = re.sub(r'<b><b>', r'<b>', text)
        text = re.sub(r'</b></b>', r'</b>', text)
        
        # Remove any remaining unclosed tags
        # Count opening and closing tags
        open_count = text.count('<b>')
        close_count = text.count('</b>')
        
        if open_count > close_count:
            # Add missing closing tags
            text += '</b>' * (open_count - close_count)
        elif close_count > open_count:
            # Remove extra closing tags
            for _ in range(close_count - open_count):
                text = text.replace('</b>', '', 1)
        
        # Escape other special characters
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;').replace('>', '&gt;')
        
        # Restore the bold tags we want
        text = text.replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>')
        
        return text
    
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
            fontSize=24,
            textColor=theme['primary_color'],
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=theme['secondary_color'],
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            alignment=TA_LEFT,
            spaceAfter=4,
            leading=14
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
        safe_name = cls.clean_html(candidate_name.upper())
        name = Paragraph(safe_name, name_style)
        elements.append(name)
        
        # Target company
        safe_company = cls.clean_html(company_name)
        target = Paragraph(
            f"<i>Optimized for: {safe_company}</i>",
            styles['Normal']
        )
        elements.append(target)
        elements.append(Spacer(1, 15))
        
        # Process resume text by sections
        try:
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
                    # Clean the title
                    clean_title = cls.clean_html(section_title)
                    clean_title = clean_title.replace('<b>', '').replace('</b>', '')
                    
                    heading = Paragraph(clean_title, heading_style)
                    elements.append(heading)
                
                # Section content
                for line in lines[1:]:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Clean the line
                    clean_line = cls.clean_html(line)
                    
                    # Handle bullet points
                    if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                        clean_line = clean_line.lstrip('•-*').strip()
                        clean_line = f"• {clean_line}"
                    
                    # Create paragraph
                    try:
                        para = Paragraph(clean_line, body_style)
                        elements.append(para)
                        elements.append(Spacer(1, 3))
                    except Exception as e:
                        # If paragraph fails, add as plain text
                        plain_text = re.sub(r'<[^>]+>', '', clean_line)
                        para = Paragraph(plain_text, body_style)
                        elements.append(para)
                        elements.append(Spacer(1, 3))
                
                elements.append(Spacer(1, 8))
        
        except Exception as e:
            # Fallback: just add plain text
            plain_text = re.sub(r'<[^>]+>', '', resume_text)
            for line in plain_text.split('\n'):
                if line.strip():
                    para = Paragraph(line.strip(), body_style)
                    elements.append(para)
                    elements.append(Spacer(1, 4))
        
        # Footer
        footer_text = f"Generated by AI Job Assistant PRO | {datetime.now().strftime('%B %Y')}"
        footer = Paragraph(
            f"<font size=8 color='gray'><i>{footer_text}</i></font>",
            styles['Normal']
        )
        elements.append(Spacer(1, 20))
        elements.append(footer)
        
        # Build PDF
        try:
            doc.build(elements)
        except Exception as e:
            # If build fails, create a simple text-only version
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            
            plain_text = re.sub(r'<[^>]+>', '', resume_text)
            for line in plain_text.split('\n'):
                if line.strip():
                    para = Paragraph(line.strip(), styles['Normal'])
                    elements.append(para)
            
            doc.build(elements)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    @classmethod
    def get_template_names(cls):
        """Get list of available template names."""
        return {key: value['name'] for key, value in cls.TEMPLATES.items()}
