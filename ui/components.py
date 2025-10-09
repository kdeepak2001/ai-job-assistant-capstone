"""Modern UI components with dynamic styling."""
import streamlit as st
import plotly.graph_objects as go

def render_ats_gauge(score: float):
    """Render a modern ATS score gauge with dynamic colors."""
    
    # Define colors dynamically
    if score < 60:
        bar_color = "#ff4b5c"  # red
    elif 60 <= score < 80:
        bar_color = "#f1c40f"  # yellow
    else:
        bar_color = "#2ecc71"  # green
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        title={'text': "ATS Match Score", "font": {"size": 22}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': bar_color, 'thickness': 0.3},
            'bgcolor': "white",
            'steps': [
                {'range': [0, 60], 'color': "#ffe6e6"},
                {'range': [60, 80], 'color': "#fff7e6"},
                {'range': [80, 100], 'color': "#e6ffed"}
            ],
        }
    ))
    
    fig.update_layout(height=280, margin=dict(t=20, b=0, l=0, r=0))
    return fig

def render_stats(stats: dict):
    """Render stats in card layout with custom styling."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 ATS Score", f"{stats.get('ats_score', 0)}%", delta="Optimized")
    
    with col2:
        st.metric("⚡ Processing Time", f"{stats.get('time', 0)}s", delta="Fast")
    
    with col3:
        st.metric("✅ Status", "Complete", delta="Ready")
