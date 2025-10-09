"""
🤖 AI Job Application Assistant PRO - Production Version
Modern UI with Real AI Agents - Complete Capstone Project
"""

import streamlit as st
import time
from datetime import datetime
import pandas as pd

# Real imports (not mocks)
from config.settings import settings
from src.parsers.pdf_parser import PDFParser
from src.agents.resume_optimizer import ResumeOptimizerAgent
from src.agents.cover_letter_agent import CoverLetterAgent
from src.agents.interview_agent import InterviewAgent
from src.agents.skill_gap_agent import SkillGapAgent
from src.agents.linkedin_agent import LinkedInAgent
from src.agents.email_agent import EmailAgent
from src.agents.career_chat_agent import CareerChatAgent
from src.utils.history_tracker import HistoryTracker
from src.utils.jd_scraper import JobDescriptionScraper
from src.utils.pdf_exporter import PDFExporter
from ui.components import render_ats_gauge, render_stats

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="AI Job Assistant PRO",
    page_icon="🤖",
    layout="wide"
)

# ============================================================================
# VALIDATE CONFIG
# ============================================================================

try:
    settings.validate()
except Exception as e:
    st.error(f"⚠️ Configuration Error: {e}")
    st.info("💡 Add GEMINI_API_KEY to your .env file")
    st.stop()

# ============================================================================
# MODERN CSS THEME
# ============================================================================

st.markdown("""
<style>
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* App background */
    .main { background: linear-gradient(180deg, #F7FBFF 0%, #FFFFFF 100%); }

    /* Header */
    .app-header {
        background: linear-gradient(90deg, rgba(102,126,234,1) 0%, rgba(118,75,162,1) 100%);
        color: white;
        padding: 28px;
        border-radius: 14px;
        box-shadow: 0 10px 30px rgba(99,102,241,0.12);
        margin-bottom: 18px;
    }
    
    .app-subheading {
        opacity: 0.95;
        margin-top: 6px;
        font-size: 0.95rem;
    }

    /* Feature badges */
    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,0.15);
        margin-right: 8px;
        font-weight: 600;
        font-size: 13px;
        backdrop-filter: blur(10px);
    }

    /* Cards */
    .card {
        background: white;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 6px 20px rgba(20,20,50,0.04);
        margin-bottom: 16px;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 10px 18px;
        border-radius: 10px;
        font-weight: 700;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102,126,234,0.3);
    }

    /* Download buttons */
    .stDownloadButton>button {
        background: linear-gradient(90deg, #11998e, #38ef7d);
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
    }

    /* Chat bubbles */
    .user-bubble {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 12px 14px;
        border-radius: 12px;
        margin: 8px 0;
        max-width: 78%;
        margin-left: auto;
        box-shadow: 0 4px 12px rgba(102,126,234,0.2);
    }
    
    .bot-bubble {
        background: #F6F8FF;
        color: #111;
        padding: 12px 14px;
        border-radius: 12px;
        margin: 8px 0;
        max-width: 78%;
        border-left: 4px solid #667eea;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
    }

    /* Text */
    .muted { color: #6b7280; font-size: 13px; }
    .mini { font-size: 12px; color: #6b7280; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #F6F8FF;
        border-radius: 12px;
        padding: 16px;
        border: 2px dashed #667eea;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        font-weight: 600;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div class='app-header'>
    <div style='display:flex;align-items:center;justify-content:space-between;'>
        <div style='flex:1'>
            <h2 style='margin:0'>🤖 AI Job Assistant PRO</h2>
            <div class='app-subheading'>Pro UX · Multi-Agent Capstone · Complete Job Application Suite</div>
        </div>
        <div style='text-align:right'>
            <span class='badge'>Resume</span>
            <span class='badge'>ATS</span>
            <span class='badge'>LinkedIn</span>
            <span class='badge'>Chat AI</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Generate", use_container_width=True):
            st.session_state._trigger_generate = True
    
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            for k in list(st.session_state.keys()):
                if k.startswith('_'):
                    continue
                del st.session_state[k]
            st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Overview")
    
    stats = HistoryTracker.get_stats()
    st.metric("Applications", stats['total_applications'])
    st.metric("Avg ATS Score", f"{stats['avg_ats_score']:.1f}%")
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    st.info(f"**Model:** {settings.MODEL_NAME}")
    st.info(f"**Temp:** {settings.TEMPERATURE}")

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================

if 'chat_agent' not in st.session_state:
    st.session_state.chat_agent = CareerChatAgent()

if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

# ============================================================================
# MAIN LAYOUT - 3 COLUMNS
# ============================================================================

left, center, right = st.columns([3, 4, 2], gap='large')

# ============================================================================
# LEFT COLUMN - INPUTS
# ============================================================================

with left:
    st.markdown("### 📤 Inputs & Uploads")
    
    # Job scraper
    with st.expander("🌐 Scrape from URL", expanded=False):
        jd_url = st.text_input("Job URL", placeholder="https://...")
        if st.button("🔍 Scrape"):
            if jd_url:
                with st.spinner("Scraping..."):
                    result = JobDescriptionScraper.scrape_from_url(jd_url)
                    if result['success']:
                        st.success("✅ Scraped!")
                        st.session_state.scraped_jd = result['job_description']
                    else:
                        st.error(f"Failed: {result['error']}")
    
    # Input method
    input_method = st.radio("Input Method:", ["📝 Paste Text", "📄 Upload PDFs"], horizontal=True)

    if input_method == "📝 Paste Text":
        resume_text = st.text_area(
            "Resume",
            height=200,
            value=st.session_state.get('resume_text', ''),
            placeholder="Paste your resume..."
        )
        jd_text = st.text_area(
            "Job Description",
            height=200,
            value=st.session_state.get('scraped_jd', ''),
            placeholder="Paste JD..."
        )
    else:
        resume_file = st.file_uploader("Resume PDF", type=['pdf'], key="resume_upload")
        if resume_file:
            st.success(f"✅ {resume_file.name}")
        
        jd_file = st.file_uploader("JD PDF", type=['pdf'], key="jd_upload")
        if jd_file:
            st.success(f"✅ {jd_file.name}")

    st.markdown("---")
    
    # Company & role
    company = st.text_input("🏢 Company", placeholder="e.g., Google")
    job_title = st.text_input("💼 Job Title", placeholder="e.g., Data Analyst")

    st.markdown("---")
    
    # Options
    st.markdown("### ⚙️ Options")
    col_a, col_b = st.columns(2)
    
    with col_a:
        strict_ats = st.checkbox("ATS Strict Mode", value=True)
    
    with col_b:
        include_cover = st.checkbox("Include Cover", value=True)

    st.markdown("---")
    
    # Generate button
    gen_btn = st.button("🚀 Generate All Materials", use_container_width=True, type="primary")

# ============================================================================
# CENTER COLUMN - PREVIEW
# ============================================================================

with center:
    st.markdown("### 📄 Live Preview")
    
    if 'optimized_resume' in st.session_state:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**✅ Optimized Resume**")
            st.text_area(
                "Preview",
                value=st.session_state.optimized_resume,
                height=300,
                disabled=True,
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("💡 No materials generated yet. Fill inputs and press Generate.")

    st.markdown("---")
    
    # ATS Score
    st.markdown("### 📈 ATS Score & Progress")
    
    if 'ats_score' in st.session_state:
        ats = st.session_state.ats_score
        
        # Use the gauge from components
        st.plotly_chart(render_ats_gauge(ats), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("ATS Score", f"{ats}%")
        with col2:
            st.metric("Time", f"{st.session_state.get('processing_time', 0)}s")
    else:
        st.progress(0)
        st.caption("Generate materials to see ATS score")

    st.markdown("---")
    
    # Suggestions
    st.markdown("### ✨ Quick Suggestions")
    
    if 'skill_gap' in st.session_state:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(st.session_state.skill_gap[:500] + "...")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.caption("Skill gap analysis will appear here")

# ============================================================================
# RIGHT COLUMN - HELPERS
# ============================================================================

with right:
    st.markdown("### 🛠️ Helpers")
    
    st.markdown("**PDF Template**")
    template_options = PDFExporter.get_template_names()
    template = st.selectbox(
        "Choose style",
        options=list(template_options.keys()),
        format_func=lambda x: template_options[x],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("**Quick Downloads**")
    
    if st.button("📄 Resume TXT", use_container_width=True):
        if 'optimized_resume' in st.session_state:
            st.download_button(
                "⬇️ Download",
                st.session_state.optimized_resume,
                file_name="resume.txt",
                use_container_width=True
            )
    
    if st.button("📄 Resume PDF", use_container_width=True):
        if 'optimized_resume' in st.session_state:
            try:
                pdf_bytes = PDFExporter.export(
                    st.session_state.optimized_resume,
                    template=template,
                    candidate_name=company,
                    company_name=company
                )
                st.download_button(
                    "⬇️ Download PDF",
                    data=pdf_bytes,
                    file_name=f"resume_{company}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"PDF error: {str(e)}")
    
    st.markdown("---")
    st.markdown('<div class="muted">💡 Use Career Chat tab for instant advice</div>', unsafe_allow_html=True)

# ============================================================================
# GENERATION LOGIC
# ============================================================================

if gen_btn or st.session_state.get('_trigger_generate', False):
    st.session_state._trigger_generate = False
    
    # Validation
    missing = []
    
    if input_method == "📝 Paste Text":
        if not resume_text:
            missing.append('resume')
        if not jd_text:
            missing.append('job description')
        resume_text_val = resume_text
        jd_text_val = jd_text
    else:
        if not resume_file:
            missing.append('resume PDF')
        if not jd_file:
            missing.append('JD PDF')
    
    if not company:
        missing.append('company')
    if not job_title:
        missing.append('job title')
    
    if missing:
        st.error(f"❌ Please provide: {', '.join(missing)}")
    else:
        with st.spinner('🤖 AI agents are processing...'):
            progress = st.progress(0)
            status = st.empty()
            
            start_time = time.time()
            
            try:
                # Extract PDFs if needed
                if input_method == "📄 Upload PDFs":
                    status.text("📄 Extracting resume...")
                    progress.progress(15)
                    resume_text_val = PDFParser.extract_text(resume_file)
                    
                    if not PDFParser.validate_pdf(resume_text_val):
                        st.error("❌ Resume PDF extraction failed")
                        st.stop()
                    
                    status.text("📄 Extracting JD...")
                    progress.progress(20)
                    jd_text_val = PDFParser.extract_text(jd_file)
                    
                    if not PDFParser.validate_pdf(jd_text_val):
                        st.error("❌ JD PDF extraction failed")
                        st.stop()
                
                # Store in session
                st.session_state.resume_text = resume_text_val
                st.session_state.jd_text = jd_text_val
                st.session_state.company_name = company
                st.session_state.job_title = job_title
                
                # Initialize agents
                status.text("🤖 Initializing AI agents...")
                progress.progress(25)
                
                resume_agent = ResumeOptimizerAgent()
                cover_agent = CoverLetterAgent()
                interview_agent = InterviewAgent()
                skill_gap_agent = SkillGapAgent()
                linkedin_agent = LinkedInAgent()
                email_agent = EmailAgent()
                
                # Resume optimization
                status.text("✍️ Optimizing resume...")
                progress.progress(40)
                resume_result = resume_agent.optimize(resume_text_val, jd_text_val)
                st.session_state.optimized_resume = resume_result['optimized_resume']
                st.session_state.ats_score = resume_result['ats_score']
                
                # Cover letter
                if include_cover:
                    status.text("✍️ Writing cover letter...")
                    progress.progress(55)
                    st.session_state.cover_letter = cover_agent.generate(
                        resume_text_val, jd_text_val, company, job_title
                    )
                
                # Interview prep
                status.text("💡 Preparing interview...")
                progress.progress(70)
                st.session_state.interview_prep = interview_agent.generate(
                    resume_text_val, jd_text_val, job_title
                )
                
                # Skill gap
                status.text("🔍 Analyzing skill gaps...")
                progress.progress(80)
                st.session_state.skill_gap = skill_gap_agent.analyze(
                    resume_text_val, jd_text_val
                )
                
                # LinkedIn
                status.text("💼 Optimizing LinkedIn...")
                progress.progress(90)
                st.session_state.linkedin_about = linkedin_agent.generate_about_section(
                    resume_text_val, job_title
                )
                st.session_state.linkedin_headline = linkedin_agent.generate_headline(
                    resume_text_val, job_title
                )
                
                # Emails
                status.text("📧 Generating emails...")
                progress.progress(95)
                st.session_state.followup_email = email_agent.generate_followup(
                    company, job_title
                )
                
                # Complete
                progress.progress(100)
                elapsed = round(time.time() - start_time, 2)
                st.session_state.processing_time = elapsed
                
                # Save to history
                HistoryTracker.add_application({
                    'company': company,
                    'role': job_title,
                    'ats_score': st.session_state.ats_score,
                    'processing_time': elapsed
                })
                
                status.empty()
                progress.empty()
                
                st.success(f"🎉 Complete! ATS {st.session_state.ats_score}% | {elapsed}s")
                st.balloons()
                time.sleep(1)
                st.rerun()
                
            except Exception as e:
                status.empty()
                progress.empty()
                st.error(f"❌ Error: {str(e)}")
                st.exception(e)

# ============================================================================
# TABS FOR DETAILED RESULTS
# ============================================================================

tabs = st.tabs(["📊 Results", "🔍 Skill Gap", "💼 LinkedIn", "💬 Career Chat", "📈 History"])

# TAB 1: Results
with tabs[0]:
    st.markdown("## 📊 Results & Export")
    
    if 'optimized_resume' in st.session_state:
        
        # Stats cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("ATS Score", f"{st.session_state.ats_score}%", delta="Optimized")
        
        with col2:
            st.metric("Processing", f"{st.session_state.processing_time}s", delta="Fast")
        
        with col3:
            st.metric("Status", "Complete", delta="Ready")
        
        st.markdown("---")
        
        # Resume
        with st.expander("📄 **Optimized Resume**", expanded=True):
            st.markdown(st.session_state.optimized_resume)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    "⬇️ Download TXT",
                    st.session_state.optimized_resume,
                    file_name=f"resume_{company}.txt",
                    key="dl_resume_txt"
                )
            
            with col2:
                try:
                    pdf_bytes = PDFExporter.export(
                        st.session_state.optimized_resume,
                        template='modern',
                        candidate_name=company,
                        company_name=company
                    )
                    st.download_button(
                        "⬇️ Download PDF",
                        data=pdf_bytes,
                        file_name=f"resume_{company}.pdf",
                        mime="application/pdf",
                        key="dl_resume_pdf"
                    )
                except:
                    pass
        
        # Cover Letter
        if 'cover_letter' in st.session_state:
            with st.expander("✉️ **Cover Letter**"):
                st.markdown(st.session_state.cover_letter)
                st.download_button(
                    "⬇️ Download",
                    st.session_state.cover_letter,
                    file_name=f"cover_{company}.txt",
                    key="dl_cover"
                )
        
        # Interview
        with st.expander("💼 **Interview Prep**"):
            st.markdown(st.session_state.interview_prep)
            st.download_button(
                "⬇️ Download",
                st.session_state.interview_prep,
                file_name="interview_prep.txt",
                key="dl_interview"
            )
    
    else:
        st.info("👈 Generate materials first")

# TAB 2: Skill Gap
with tabs[1]:
    st.markdown("## 🔍 Skill Gap Analysis")
    
    if 'skill_gap' in st.session_state:
        st.markdown(st.session_state.skill_gap)
        st.download_button(
            "⬇️ Download Report",
            st.session_state.skill_gap,
            file_name="skill_gap.txt"
        )
    else:
        st.info("👈 Generate first")

# TAB 3: LinkedIn
with tabs[2]:
    st.markdown("## 💼 LinkedIn Optimizer")
    
    if 'linkedin_headline' in st.session_state:
        with st.expander("📝 **Headline**", expanded=True):
            st.markdown(st.session_state.linkedin_headline)
            st.download_button(
                "⬇️ Download",
                st.session_state.linkedin_headline,
                file_name="linkedin_headline.txt"
            )
        
        with st.expander("📄 **About Section**", expanded=True):
            st.markdown(st.session_state.linkedin_about)
            st.download_button(
                "⬇️ Download",
                st.session_state.linkedin_about,
                file_name="linkedin_about.txt"
            )
        
        st.markdown("---")
        st.markdown("### 📧 Email Templates")
        
        with st.expander("📧 **Follow-up Email**"):
            st.markdown(st.session_state.followup_email)
            st.download_button(
                "⬇️ Download",
                st.session_state.followup_email,
                file_name="followup_email.txt"
            )
    else:
        st.info("👈 Generate first")

# TAB 4: Career Chat
with tabs[3]:
    st.markdown("## 💬 Career Chat AI")
    st.markdown("Ask me anything about your career!")
    
    # Display messages
    for msg in st.session_state.chat_messages:
        if msg['role'] == 'user':
            st.markdown(
                f'<div class="user-bubble">🧑 {msg["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="bot-bubble">🤖 {msg["content"]}</div>',
                unsafe_allow_html=True
            )
    
    # Chat input
    col1, col2 = st.columns([5, 1])
    
    with col1:
        q = st.text_input("Your question:", key='chat_input', label_visibility="collapsed")
    
    with col2:
        if st.button("Send"):
            if q:
                ctx = st.session_state.get('resume_text')
                resp = st.session_state.chat_agent.chat(q, ctx)
                
                st.session_state.chat_messages.append({'role': 'user', 'content': q})
                st.session_state.chat_messages.append({'role': 'assistant', 'content': resp})
                
                st.rerun()
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_messages = []
        st.session_state.chat_agent.reset_conversation()
        st.rerun()

# TAB 5: History
with tabs[4]:
    st.markdown("## 📈 History & Analytics")
    
    hist = HistoryTracker.get_all()
    
    if hist:
        stats = HistoryTracker.get_stats()
        
        # Stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Apps", stats['total_applications'])
        
        with col2:
            st.metric("Avg ATS", f"{stats['avg_ats_score']:.1f}%")
        
        with col3:
            st.metric("Companies", len(stats['companies']))
        
        st.markdown("---")
        
        # Table
        df = pd.DataFrame(hist)
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
        
        display_df = df[['timestamp', 'company', 'role', 'ats_score', 'processing_time']]
        display_df.columns = ['Date', 'Company', 'Role', 'ATS Score', 'Time (s)']
        
        st.dataframe(display_df, use_container_width=True)
    
    else:
        st.info("No history yet")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown('<div class="footer">© 2025 AI Job Assistant Pro • All Rights Reserved</div>', unsafe_allow_html=True)

