import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.ats.matcher import analyze_resume_jd

st.set_page_config(
    page_title="CampusMind | Placement & Career Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom Enterprise Dark-Neon CSS ───
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #0f172a 0%, #090d16 55%, #05070e 100%);
        color: #f8fafc;
    }
    .campus-banner {
        background: linear-gradient(135deg, rgba(15,23,42,0.95) 0%, rgba(14,116,144,0.85) 100%);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-left: 5px solid #38bdf8;
        border-radius: 14px;
        padding: 22px 28px;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
    }
    .campus-title {
        font-size: 1.85rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(90deg, #38bdf8, #34d399, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .campus-sub {
        color: #94a3b8;
        font-size: 0.92rem;
        margin-top: 6px;
    }
    .kpi-card {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-top: 3px solid #38bdf8;
        border-radius: 12px;
        padding: 16px 18px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.3);
    }
    .kpi-label {
        color: #94a3b8;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
    }
    .kpi-value {
        color: #f8fafc;
        font-size: 1.25rem;
        font-weight: 800;
        margin-top: 4px;
    }
    .panel-header {
        font-size: 1.05rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 4px;
    }
    .panel-caption {
        font-size: 0.82rem;
        color: #94a3b8;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─── Sidebar ───
with st.sidebar:
    st.markdown("### 🎓 CampusMind Hub")
    st.caption("Placement & Career Intelligence Platform")
    st.divider()
    st.markdown("**🟢 System Status:** `ONLINE`")
    st.markdown("**⚡ Engine:** `TF-IDF Cosine Scorer`")
    st.divider()
    st.markdown("#### 🚀 Core Modules")
    st.markdown("- 📄 AI Resume ATS Matcher")
    st.markdown("- 📊 Placement Application Tracker")
    st.markdown("- 💻 Coding Progress Analytics")
    st.divider()
    st.caption("Built by Aditya Mitra • KIIT CSE")

# ─── Hero Banner ───
st.markdown(
    """
    <div class="campus-banner">
        <div class="campus-title">🎓 CampusMind — Placement & Career Intelligence Center</div>
        <div class="campus-sub">
            AI-Powered Resume ATS Optimization • Keyword Gap Analysis • Recruiter-Friendly Placement Analytics
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── Tabs ───
tab1, tab2, tab3 = st.tabs(
    [
        "📄 AI Resume & JD ATS Matcher",
        "📊 Placement & Application Tracker",
        "💻 Coding Progress Analytics",
    ]
)

# ═══════════════════════════════════════════════════════════
# TAB 1: AI RESUME ATS MATCHER
# ═══════════════════════════════════════════════════════════
with tab1:
    st.markdown("#### ⚡ Paste Resume & Target Job Description")
    
    col_res, col_jd = st.columns(2, gap="large")
    with col_res:
        resume_input = st.text_area(
            "📄 Applicant Resume Text:",
            value="Experienced Software Engineer skilled in Python, FastAPI, Docker, PostgreSQL, React, and Git workflows. Built scalable microservices and REST APIs.",
            height=210,
        )
    with col_jd:
        jd_input = st.text_area(
            "🎯 Target Job Description (JD):",
            value="Looking for a backend software engineer proficient in Python, FastAPI, Docker, Kubernetes, AWS, and PostgreSQL database management.",
            height=210,
        )

    if st.button("🚀 Analyze ATS Compatibility", use_container_width=True):
        if resume_input and jd_input:
            res = analyze_resume_jd(resume_input, jd_input)
            score = res["match_score"]

            st.write("")
            k1, k2, k3 = st.columns(3)
            k1.markdown(f'<div class="kpi-card"><div class="kpi-label">ATS Match Score</div><div class="kpi-value">{score}%</div></div>', unsafe_allow_html=True)
            k2.markdown(f'<div class="kpi-card" style="border-top-color:#34d399;"><div class="kpi-label">Matched Keywords</div><div class="kpi-value">{len(res["matched_keywords"])} Found</div></div>', unsafe_allow_html=True)
            k3.markdown(f'<div class="kpi-card" style="border-top-color:#f43f5e;"><div class="kpi-label">Missing Keywords</div><div class="kpi-value">{len(res["missing_keywords"])} Missing</div></div>', unsafe_allow_html=True)

            st.write("")
            if score >= 75:
                st.success(res["recommendation"])
            elif score >= 45:
                st.warning(res["recommendation"])
            else:
                st.error(res["recommendation"])

            g1, g2 = st.columns(2, gap="large")
            with g1:
                st.markdown("##### ✅ Matched Resume Keywords")
                if res["matched_keywords"]:
                    st.pills("Matched", res["matched_keywords"], selection_mode="disabled")
                else:
                    st.info("No matching keywords found.")
            with g2:
                st.markdown("##### ❌ Missing Keywords to Add")
                if res["missing_keywords"]:
                    st.pills("Missing", res["missing_keywords"], selection_mode="disabled")
                else:
                    st.success("Zero missing keywords! Perfect match.")
        else:
            st.error("Please provide both resume text and job description.")

# ═══════════════════════════════════════════════════════════
# TAB 2: PLACEMENT & APPLICATION TRACKER
# ═══════════════════════════════════════════════════════════
with tab2:
    st.markdown("#### 📊 On-Campus & Off-Campus Application Pipeline")
    
    app_data = [
        {"Company": "Google", "Role": "Software Engineering Intern", "Status": "Online Assessment (OA)", "Package": "24 LPA", "Date": "2026-03-10"},
        {"Company": "Microsoft", "Role": "SDE Intern", "Status": "Interview Scheduled", "Package": "22 LPA", "Date": "2026-03-14"},
        {"Company": "Amazon", "Role": "Cloud Support Associate", "Status": "Applied", "Package": "18 LPA", "Date": "2026-03-01"},
        {"Company": "Goldman Sachs", "Role": "Engineering Analyst", "Status": "Offer Received", "Package": "26 LPA", "Date": "2026-02-15"},
    ]
    import pandas as pd
    st.dataframe(pd.DataFrame(app_data), use_container_width=True)

# ═══════════════════════════════════════════════════════════
# TAB 3: CODING PROGRESS ANALYTICS
# ═══════════════════════════════════════════════════════════
with tab3:
    st.markdown("#### 💻 DSA & Competitive Programming Analytics")
    c1, c2, c3 = st.columns(3)
    c1.metric("LeetCode Solved", "480+", "▲ 15 this week")
    c2.metric("Codeforces Rating", "1420 (Specialist)", "▲ 65 pts")
    c3.metric("Contest Accuracy", "88.5%", "Consistent")

    topics = ["Arrays & Hashing", "Two Pointers", "Sliding Window", "Binary Search", "Trees", "Graphs", "Dynamic Programming"]
    solved_counts = [95, 60, 45, 50, 70, 40, 55]
    
    fig_dsa = px.bar(
        x=topics, y=solved_counts, labels={"x": "DSA Topic", "y": "Problems Solved"},
        color=solved_counts, color_continuous_scale="Teal"
    )
    fig_dsa.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.5)",
        font={"color": "#f8fafc"},
        height=330,
        margin=dict(l=10, r=10, t=15, b=40)
    )
    st.plotly_chart(fig_dsa, use_container_width=True, config={"displayModeBar": False})