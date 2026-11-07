import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
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
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-top: 3px solid #38bdf8;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
        margin-bottom: 12px;
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
        font-size: 1.4rem;
        font-weight: 800;
        margin-top: 4px;
    }
    .kw-badge-match {
        display: inline-block;
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(52, 211, 153, 0.4);
        border-radius: 999px;
        padding: 5px 13px;
        margin: 4px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .kw-badge-miss {
        display: inline-block;
        background: rgba(244, 63, 94, 0.15);
        color: #fb7185;
        border: 1px solid rgba(251, 113, 133, 0.4);
        border-radius: 999px;
        padding: 5px 13px;
        margin: 4px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .neon-table {
        width: 100%;
        border-collapse: collapse;
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 12px;
        overflow: hidden;
        margin-top: 10px;
    }
    .neon-table th {
        background: rgba(30, 41, 59, 0.9);
        color: #38bdf8;
        text-align: left;
        padding: 13px 16px;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        border-bottom: 1px solid rgba(148, 163, 184, 0.2);
    }
    .neon-table td {
        padding: 13px 16px;
        color: #e2e8f0;
        font-size: 0.9rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    }
    .status-pill {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 700;
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.35);
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
            k1.markdown(
                f'<div class="kpi-card"><div class="kpi-label">ATS Match Score</div><div class="kpi-value">{score}%</div></div>',
                unsafe_allow_html=True,
            )
            k2.markdown(
                f'<div class="kpi-card" style="border-top-color:#34d399;"><div class="kpi-label">Matched Keywords</div><div class="kpi-value">{len(res["matched_keywords"])} Found</div></div>',
                unsafe_allow_html=True,
            )
            k3.markdown(
                f'<div class="kpi-card" style="border-top-color:#f43f5e;"><div class="kpi-label">Missing Keywords</div><div class="kpi-value">{len(res["missing_keywords"])} Missing</div></div>',
                unsafe_allow_html=True,
            )

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
                    badges_html = "".join(
                        [f'<span class="kw-badge-match">{kw}</span>' for kw in res["matched_keywords"]]
                    )
                    st.markdown(f"<div>{badges_html}</div>", unsafe_allow_html=True)
                else:
                    st.info("No matching keywords found.")
            with g2:
                st.markdown("##### ❌ Missing Keywords to Add")
                if res["missing_keywords"]:
                    miss_html = "".join(
                        [f'<span class="kw-badge-miss">{kw}</span>' for kw in res["missing_keywords"]]
                    )
                    st.markdown(f"<div>{miss_html}</div>", unsafe_allow_html=True)
                else:
                    st.success("Zero missing keywords! Perfect match.")
        else:
            st.error("Please provide both resume text and job description.")

# ═══════════════════════════════════════════════════════════
# TAB 2: PLACEMENT & APPLICATION TRACKER
# ═══════════════════════════════════════════════════════════
with tab2:
    st.markdown("#### 📊 On-Campus & Off-Campus Application Pipeline")

    m1, m2, m3, m4 = st.columns(4)
    m1.markdown('<div class="kpi-card"><div class="kpi-label">Total Applications</div><div class="kpi-value">24</div></div>', unsafe_allow_html=True)
    m2.markdown('<div class="kpi-card" style="border-top-color:#818cf8;"><div class="kpi-label">Online Assessments</div><div class="kpi-value">9 Cleared</div></div>', unsafe_allow_html=True)
    m3.markdown('<div class="kpi-card" style="border-top-color:#f59e0b;"><div class="kpi-label">Active Interviews</div><div class="kpi-value">4 Scheduled</div></div>', unsafe_allow_html=True)
    m4.markdown('<div class="kpi-card" style="border-top-color:#34d399;"><div class="kpi-label">Offers Received</div><div class="kpi-value">2 Offers</div></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <table class="neon-table">
            <thead>
                <tr>
                    <th>Company</th>
                    <th>Target Role</th>
                    <th>Pipeline Stage</th>
                    <th>CTC Package</th>
                    <th>Updated Date</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><b>Goldman Sachs</b></td>
                    <td>Engineering Analyst</td>
                    <td><span class="status-pill" style="color:#34d399;border-color:#34d399;background:rgba(52,211,153,0.15);">Offer Received</span></td>
                    <td>26 LPA</td>
                    <td>2026-02-15</td>
                </tr>
                <tr>
                    <td><b>Microsoft</b></td>
                    <td>SDE Intern / FTE</td>
                    <td><span class="status-pill" style="color:#fbbf24;border-color:#fbbf24;background:rgba(251,191,36,0.15);">Interview Scheduled</span></td>
                    <td>22 LPA</td>
                    <td>2026-03-14</td>
                </tr>
                <tr>
                    <td><b>Google</b></td>
                    <td>Software Engineering Intern</td>
                    <td><span class="status-pill">Online Assessment (OA)</span></td>
                    <td>24 LPA</td>
                    <td>2026-03-10</td>
                </tr>
                <tr>
                    <td><b>Amazon</b></td>
                    <td>SDE-1 Backend</td>
                    <td><span class="status-pill" style="color:#c084fc;border-color:#c084fc;background:rgba(192,132,252,0.15);">Applied</span></td>
                    <td>18 LPA</td>
                    <td>2026-03-01</td>
                </tr>
            </tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )

# ═══════════════════════════════════════════════════════════
# TAB 3: CODING PROGRESS ANALYTICS
# ═══════════════════════════════════════════════════════════
with tab3:
    st.markdown("#### 💻 DSA & Competitive Programming Analytics")
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="kpi-card"><div class="kpi-label">LeetCode Solved</div><div class="kpi-value">480+ <span style="font-size:0.8rem;color:#34d399;">▲ +15/wk</span></div></div>', unsafe_allow_html=True)
    c2.markdown('<div class="kpi-card" style="border-top-color:#34d399;"><div class="kpi-label">Codeforces Rating</div><div class="kpi-value">1420 <span style="font-size:0.8rem;color:#38bdf8;">Specialist</span></div></div>', unsafe_allow_html=True)
    c3.markdown('<div class="kpi-card" style="border-top-color:#818cf8;"><div class="kpi-label">Contest Accuracy</div><div class="kpi-value">88.5% <span style="font-size:0.8rem;color:#a78bfa;">Consistent</span></div></div>', unsafe_allow_html=True)

    topics = ["Arrays & Hashing", "Two Pointers", "Sliding Window", "Binary Search", "Trees", "Graphs", "Dynamic Programming"]
    solved_counts = [95, 60, 45, 50, 70, 40, 55]

    fig_dsa = go.Figure(
        data=[
            go.Bar(
                x=topics,
                y=solved_counts,
                marker=dict(
                    color=solved_counts,
                    colorscale="Tealgrn",
                    line=dict(color="rgba(56,189,248,0.6)", width=1.2),
                ),
                text=solved_counts,
                textposition="outside",
            )
        ]
    )
    fig_dsa.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.5)",
        font=dict(color="#f8fafc"),
        xaxis=dict(title="DSA Topic", gridcolor="rgba(148,163,184,0.1)"),
        yaxis=dict(title="Problems Solved", gridcolor="rgba(148,163,184,0.15)", range=[0, 115]),
        height=360,
        margin=dict(l=10, r=10, t=25, b=40),
    )
    st.plotly_chart(fig_dsa, use_container_width=True, config={"displayModeBar": False})