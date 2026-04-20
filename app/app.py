from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from db import (
    DB_PATH,
    add_reward_points,
    assign_basic_badges,
    complete_module_if_passed,
    create_quiz_attempt,
    fetch_all,
    fetch_one,
    finalize_quiz_attempt,
    get_connection,
    get_course,
    get_courses,
    get_full_quiz,
    get_latest_quiz_attempt,
    get_module,
    get_module_feedback,
    get_module_progress,
    get_modules_by_course,
    get_question_options,
    get_quiz_by_module,
    get_student,
    get_student_badges,
    get_student_dashboard,
    get_student_total_points,
    get_teacher_module_overview,
    get_teacher_student_overview,
    get_users_by_role,
    is_module_unlocked,
    log_rag_interaction,
    mark_module_accessed,
    save_material_feedback,
    save_quiz_response,
)

from rag.rag_page import render_rag_page

APP_USERNAME = ""
APP_PASSWORD = ""

st.set_page_config(
    page_title="UAb Pedagogical Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


def normalize_pct(value: float | int | None) -> float | None:
    if value is None:
        return None
    value = float(value)
    if value <= 1:
        return round(value * 100, 2)
    return round(value, 2)


def parse_json_list(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except json.JSONDecodeError:
        return []


def resolve_logo_path() -> Path | None:
    base = Path(__file__).resolve().parent
    candidates = [
        base / "img" / "logo_UAb_novo.png",
        base / "logo_UAb_novo.png",
        Path.cwd() / "img" / "logo_UAb_novo.png",
        Path.cwd() / "logo_UAb_novo.png",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


LOGO_PATH = resolve_logo_path()


def inject_css() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(191, 219, 254, 0.35), transparent 26%),
                    radial-gradient(circle at top right, rgba(147, 197, 253, 0.28), transparent 22%),
                    linear-gradient(180deg, #f8fbff 0%, #f4f7fb 45%, #eef3f9 100%);
            }

            .block-container {
                max-width: 1320px;
                padding-top: 1.1rem;
                padding-bottom: 2rem;
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #0f172a 0%, #172554 60%, #1d4ed8 100%);
                border-right: 1px solid rgba(255,255,255,0.08);
            }

            [data-testid="stSidebar"] * {
                color: #f8fafc !important;
            }

            .topbar {
                padding: 1.1rem 1.3rem;
                border-radius: 28px;
                background: linear-gradient(135deg, rgba(255,255,255,0.96) 0%, rgba(241,245,249,0.93) 100%);
                border: 1px solid rgba(148, 163, 184, 0.18);
                box-shadow: 0 22px 50px rgba(15, 23, 42, 0.09);
                margin-bottom: 1.15rem;
            }

            .hero-card {
                padding: 1.45rem 1.55rem;
                border-radius: 30px;
                background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 42%, #2563eb 72%, #60a5fa 100%);
                color: white;
                box-shadow: 0 24px 48px rgba(37, 99, 235, 0.22);
                min-height: 188px;
            }

            .hero-card h1 {
                margin: 0;
                font-size: 2.2rem;
                line-height: 1.05;
                font-weight: 800;
                letter-spacing: -0.02em;
                color: white !important;
            }

            .hero-card p {
                margin-top: 0.7rem;
                margin-bottom: 0;
                color: rgba(255,255,255,0.92) !important;
                font-size: 1rem;
                line-height: 1.5;
            }

            .hero-tag {
                display: inline-block;
                padding: 0.36rem 0.72rem;
                border-radius: 999px;
                background: rgba(255,255,255,0.14);
                border: 1px solid rgba(255,255,255,0.20);
                margin-bottom: 0.7rem;
                font-size: 0.82rem;
                font-weight: 700;
                letter-spacing: 0.02em;
                color: white !important;
            }

            .metric-card {
                background: linear-gradient(180deg, rgba(255,255,255,0.96) 0%, rgba(248,250,252,0.98) 100%);
                border: 1px solid rgba(148, 163, 184, 0.14);
                border-radius: 24px;
                padding: 1rem 1.08rem;
                box-shadow: 0 16px 36px rgba(15, 23, 42, 0.06);
                min-height: 130px;
            }

            .metric-label { color: #64748b; font-size: 0.88rem; font-weight: 600; margin-bottom: 0.3rem; }
            .metric-value { color: #0f172a; font-size: 1.95rem; font-weight: 800; letter-spacing: -0.02em; }
            .metric-note { color: #475569; font-size: 0.85rem; margin-top: 0.35rem; }

            .glass-card {
                background: rgba(255,255,255,0.92);
                border: 1px solid rgba(148, 163, 184, 0.14);
                border-radius: 26px;
                padding: 1.15rem 1.2rem;
                box-shadow: 0 20px 40px rgba(15, 23, 42, 0.06);
            }

            .module-card {
                background: linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(248,250,252,1) 100%);
                border: 1px solid rgba(148, 163, 184, 0.14);
                border-radius: 26px;
                padding: 1.12rem 1.12rem 1rem 1.12rem;
                box-shadow: 0 14px 36px rgba(15, 23, 42, 0.06);
                margin-bottom: 0.95rem;
            }

            .module-title { color: #0f172a; font-size: 1.1rem; font-weight: 800; margin-bottom: 0.3rem; }
            .module-desc { color: #475569; font-size: 0.94rem; line-height: 1.45; min-height: 42px; }

            .pill {
                display: inline-block;
                padding: 0.3rem 0.62rem;
                border-radius: 999px;
                font-size: 0.78rem;
                font-weight: 700;
                margin-right: 0.45rem;
                margin-top: 0.35rem;
            }

            .pill-blue { background: #dbeafe; color: #1d4ed8; }
            .pill-green { background: #dcfce7; color: #166534; }
            .pill-amber { background: #fef3c7; color: #92400e; }
            .pill-slate { background: #e2e8f0; color: #334155; }
            .pill-rose { background: #ffe4e6; color: #be123c; }

            .badge-chip {
                display: inline-block;
                padding: 0.42rem 0.72rem;
                border-radius: 999px;
                margin-right: 0.5rem;
                margin-bottom: 0.5rem;
                background: #eef4ff;
                border: 1px solid #c7d2fe;
                color: #1d4ed8;
                font-size: 0.84rem;
                font-weight: 700;
            }

            .section-title {
                color: #0f172a;
                font-size: 1.18rem;
                font-weight: 800;
                letter-spacing: -0.01em;
                margin-top: 0.35rem;
                margin-bottom: 0.85rem;
            }

            .soft-panel {
                padding: 1rem 1.05rem;
                border-radius: 22px;
                background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
                border: 1px solid rgba(148, 163, 184, 0.14);
            }

            .small-muted { color: #64748b; font-size: 0.86rem; }
            .logo-box { display: flex; justify-content: center; align-items: center; padding: 0.2rem 0 0.6rem 0; }

            div.stButton > button,
            button[data-testid="baseButton-secondary"] {
                border-radius: 14px;
                border: 1px solid rgba(37,99,235,.18);
                padding: .65rem 1rem;
                font-weight: 700;
                background: linear-gradient(180deg, #ffffff, #f8fbff);
                color: #0f172a !important;
            }

            div.stButton > button[kind="primary"],
            button[data-testid="baseButton-primary"] {
                background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
                color: #ffffff !important;
                border: 1px solid rgba(37,99,235,.32) !important;
            }

            div.stButton > button[kind="primary"] *,
            button[data-testid="baseButton-primary"] * {
                color: #ffffff !important;
            }

            div.stButton > button:hover,
            button[data-testid="baseButton-secondary"]:hover {
                border-color: rgba(37,99,235,.32);
                color: #1d4ed8 !important;
            }

            div.stButton > button[kind="primary"]:hover,
            button[data-testid="baseButton-primary"]:hover {
                color: #ffffff !important;
                border-color: rgba(29,78,216,.55) !important;
            }

            div[data-testid="stForm"] label,
            div[data-testid="stForm"] p,
            div[data-testid="stForm"] span,
            div[data-testid="stForm"] div,
            [data-testid="stMarkdownContainer"],
            h1, h2, h3, h4, h5 {
                color: #0f172a !important;
            }
            div[data-testid="stMetric"] { background: transparent; }
            [data-testid="stSidebar"] div.stButton > button {
               background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
               color: #ffffff !important;
               border: 1px solid rgba(255,255,255,0.18) !important;
               font-weight: 700 !important;
            }
            [data-testid="stSidebar"] div.stButton > button * {
                color: #ffffff !important;
                fill: #ffffff !important;
            }
            [data-testid="stSidebar"] div.stButton > button:hover {
                background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%) !important;
                color: #ffffff !important;
            }
            [data-testid="stSidebar"] div.stButton > button:hover * {
                color: #ffffff !important;
                fill: #ffffff !important;
            }
            div[data-testid="stMetric"] label {
                color: #64748b !important;   /* título */
                font-weight: 600 !important;
            }

            div[data-testid="stMetric"] div {
                color: #0f172a !important;   /* valor principal */
                font-weight: 800 !important;
            }

            /* valor grande (ex: 100%) */
            div[data-testid="stMetricValue"] {
                color: #0f172a !important;
                font-size: 1.6rem !important;
            }

            /* delta / texto auxiliar */
            div[data-testid="stMetricDelta"] {
            color: #475569 !important;
            }      
            /* Link button do Streamlit */
            div[data-testid="stLinkButton"] a {
                background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
                color: #ffffff !important;
                border: 1px solid rgba(37,99,235,.32) !important;
                border-radius: 14px !important;
                font-weight: 700 !important;
                padding: .72rem 1rem !important;
                text-decoration: none !important;
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                box-shadow: 0 10px 24px rgba(37,99,235,.18) !important;
            }

            div[data-testid="stLinkButton"] a:hover {
                background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%) !important;
                color: #ffffff !important;
                text-decoration: none !important;
            }   

            /* ========================= */
            /* BOTÕES AZUIS CONSISTENTES */
            /* ========================= */

            div.stButton > button,
            div[data-testid="stForm"] button,
            div[data-testid="stBaseButton-secondary"] > button,
            div[data-testid="stBaseButton-primary"] > button {
                border-radius: 14px !important;
                border: 1px solid rgba(37,99,235,.28) !important;
                padding: .7rem 1rem !important;
                font-weight: 700 !important;
            }

            div.stButton > button[kind="primary"],
            div[data-testid="stForm"] button[kind="primary"],
            div[data-testid="stBaseButton-primary"] > button {
                background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
                color: #ffffff !important;
                border: 1px solid rgba(37,99,235,.35) !important;
            }

            div.stButton > button[kind="primary"] *,
            div[data-testid="stForm"] button[kind="primary"] *,
            div[data-testid="stBaseButton-primary"] > button * {
                color: #ffffff !important;
                fill: #ffffff !important;
            }

            div.stButton > button[kind="primary"]:hover,
            div[data-testid="stForm"] button[kind="primary"]:hover,
            div[data-testid="stBaseButton-primary"] > button:hover {
                background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%) !important;
                color: #ffffff !important;
            }

            div.stButton > button[kind="primary"]:hover *,
            div[data-testid="stForm"] button[kind="primary"]:hover *,
            div[data-testid="stBaseButton-primary"] > button:hover * {
                color: #ffffff !important;
                fill: #ffffff !important;
            }

            /* também força texto branco em submits de formulário */
            div[data-testid="stForm"] button {
            background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
            color: #ffffff !important;
            border: 1px solid rgba(37,99,235,.35) !important;
            }

            div[data-testid="stForm"] button * {
            color: #ffffff !important;
            fill: #ffffff !important;
            }

            /* ========================= */
            /* CAMPO COMENTÁRIO BRANCO   */
            /* ========================= */

            div[data-testid="stTextArea"] textarea {
                background: #ffffff !important;
                color: #0f172a !important;
                border: 1px solid rgba(148,163,184,.20) !important;
                border-radius: 16px !important;
                box-shadow: 0 4px 14px rgba(15,23,42,.04) !important;
            }

            div[data-testid="stTextArea"] textarea::placeholder {
                color: #64748b !important;
                opacity: 1 !important;
            }   

            div[data-testid="stTextArea"] label,
            div[data-testid="stTextArea"] p {
                color: #0f172a !important;
                font-weight: 700 !important;
            }            

            /* ========================= */
            /* RADIOS: FUNDO BRANCO      */
            /* CÍRCULO AZUL             */
            /* ========================= */

            div[data-testid="stRadio"] {
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
                padding: 0 !important;
            }

            div[data-testid="stRadio"] [role="radiogroup"] {
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
                padding: 0 !important;
                gap: .45rem !important;
            }

            /* cada opção continua branca */
            div[data-testid="stRadio"] [role="radiogroup"] > label {
                background: #ffffff !important;
                border: 1px solid rgba(148,163,184,.22) !important;
                border-radius: 14px !important;
                padding: .45rem .8rem !important;
                margin: 0 !important;
                box-shadow: 0 4px 10px rgba(15,23,42,.04) !important;
            }

            /* hover suave */
            div[data-testid="stRadio"] [role="radiogroup"] > label:hover {
                background: #f8fbff !important;
                border-color: #bfdbfe !important;
            }

            /* texto */
            div[data-testid="stRadio"] [role="radiogroup"] > label p,
            div[data-testid="stRadio"] [role="radiogroup"] > label span {
                color: #0f172a !important;
                font-weight: 700 !important;
                margin: 0 !important;
            }

            /* círculo do radio - estado normal */
            div[data-testid="stRadio"] svg {
                fill: #93c5fd !important;     /* azul claro */
                stroke: #93c5fd !important;
            }

            /* círculo do radio - selecionado */
            div[data-testid="stRadio"] input[type="radio"]:checked,
            div[data-testid="stRadio"] label:has(input[type="radio"]:checked) svg {
                fill: #1d4ed8 !important;     /* azul escuro */
                stroke: #1d4ed8 !important;
            }

            /* sidebar: opções uma por linha */
            [data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] {
                display: flex !important;
                flex-direction: column !important;
                gap: .55rem !important;
            }

            [data-testid="stSidebar"] div[data-testid="stRadio"] [role="radiogroup"] > label {
                width: 100% !important;
                min-height: 44px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: flex-start !important;
            }

            /* formulários: manter horizontal quando definido */
            div[data-testid="stForm"] div[data-testid="stRadio"] [role="radiogroup"] {
                display: flex !important;
                flex-wrap: nowrap !important;
                gap: .45rem !important;
            }

            div[data-testid="stForm"] div[data-testid="stRadio"] [role="radiogroup"] > label {
                min-width: 44px !important;
                min-height: 40px !important;
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                border-radius: 999px !important;
            }

            /* ========================= */
            /* BOTÃO ABRIR TUTOR RAG     */
            /* ========================= */

            div[data-testid="stLinkButton"] a {
                background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
                color: #ffffff !important;
                border: 1px solid rgba(37,99,235,.35) !important;
                border-radius: 14px !important;
                font-weight: 700 !important;
                padding: .72rem 1rem !important;
                text-decoration: none !important;
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                box-shadow: 0 10px 24px rgba(37,99,235,.18) !important;
            }

            div[data-testid="stLinkButton"] a:hover {
                background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%) !important;
                color: #ffffff !important;
                text-decoration: none !important;
            }

            div[data-testid="stLinkButton"] a,
            div[data-testid="stLinkButton"] a *,
            div[data-testid="stLinkButton"] a span,
            div[data-testid="stLinkButton"] a p {
                color: #ffffff !important;
                fill: #ffffff !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state() -> None:
    defaults = {
        "role": "Estudante",
        "course_id": None,
        "student_id": None,
        "page": "student_home",
        "module_id": None,
        "authenticated": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_login() -> None:
    st.markdown(
        """
        <div style="
            max-width: 460px;
            margin: 4rem auto 0 auto;
            padding: 2rem 2rem 1.5rem 2rem;
            border-radius: 28px;
            background: linear-gradient(135deg, rgba(255,255,255,0.96) 0%, rgba(241,245,249,0.94) 100%);
            border: 1px solid rgba(148,163,184,0.16);
            box-shadow: 0 24px 48px rgba(15,23,42,0.10);
            text-align: center;
        ">
            <h1 style="margin-bottom: .4rem; color: #0f172a;">UAb Analytics</h1>
            <p style="color: #475569; margin-top: 0;">
                Acesso reservado à demonstração pedagógica
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    with st.form("login_form"):
        username = st.text_input("Utilizador")
        password = st.text_input("Palavra-passe", type="password")
        submitted = st.form_submit_button("Entrar", use_container_width=True)

    if submitted:
        if username == APP_USERNAME and password == APP_PASSWORD:
            st.session_state.authenticated = True
            st.success("Autenticação efetuada com sucesso.")
            st.rerun()
        else:
            st.error("Utilizador ou palavra-passe incorretos.")

def render_topbar() -> None:
    logo_html = ""
    if LOGO_PATH:
        logo_html = f'<img src="data:image/png;base64,{logo_to_base64(LOGO_PATH)}" style="height:68px; border-radius:12px;" />'
    st.markdown(
        f"""
        <div class="topbar">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:1rem;">
                <div>
                    <div class="small-muted">Universidade Aberta · Pedagogical Analytics</div>
                    <div style="font-size:1.3rem;font-weight:800;color:#0f172a;">Learning analytics, avaliação formativa e autorregulação</div>
                </div>
                <div class="logo-box">{logo_html}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def logo_to_base64(path: Path) -> str:
    import base64
    return base64.b64encode(path.read_bytes()).decode("ascii")


def render_hero(title: str, subtitle: str, tag: str = "UAb 2026") -> None:
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-tag">{tag}</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label: str, value: str, note: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    with st.sidebar:
        if LOGO_PATH:
            st.image(str(LOGO_PATH), use_container_width=True)
        st.markdown("## UAb Analytics")
        st.caption("Progressão · Quiz · Feedback · Dashboard")

        st.session_state.role = st.radio(
            "Perfil",
            ["Estudante", "Professor"],
            index=0 if st.session_state.role == "Estudante" else 1,
            horizontal=False,
        )

        courses = get_courses()
        if not courses:
            st.error("Sem cursos ativos na base de dados.")
            st.stop()
        course_options = {c["title"]: c["id"] for c in courses}
        selected_course = st.selectbox("Unidade curricular", list(course_options.keys()))
        st.session_state.course_id = course_options[selected_course]

        if st.session_state.role == "Estudante":
            students = get_users_by_role("student")
            if not students:
                st.error("Sem estudantes na base de dados.")
                st.stop()
            student_options = {s["full_name"]: s["id"] for s in students}
            selected_student = st.selectbox("Estudante", list(student_options.keys()))
            st.session_state.student_id = student_options[selected_student]

            if st.button("Ver percurso completo", use_container_width=True):
                st.session_state.page = "student_home"

            has_current_module = st.session_state.module_id is not None

            if st.button("🤖 Tutor RAG", use_container_width=True):
                st.session_state.page = "rag"
                st.rerun()            

        else:
            teachers = get_users_by_role("teacher")
            if teachers:
                st.selectbox("Docente", [t["full_name"] for t in teachers], disabled=True)
            st.divider()
            if st.button("📊 Dashboard docente", use_container_width=True):
                st.session_state.page = "teacher_home"

        st.caption(f"Base ativa: {DB_PATH}")


def get_feedback_summary(module_id: int) -> dict[str, Any]:
    feedback = get_module_feedback(module_id)
    if not feedback:
        return {"count": 0, "avg_clarity": None, "avg_usefulness": None}
    return {
        "count": len(feedback),
        "avg_clarity": sum(f["clarity_rating"] for f in feedback) / len(feedback),
        "avg_usefulness": sum(f["usefulness_rating"] for f in feedback) / len(feedback),
    }


def get_material_feedback_for_student(student_id: int, module_id: int) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM material_feedback WHERE student_id = ? AND module_id = ?",
            (student_id, module_id),
        ).fetchone()
    return dict(row) if row else None


def get_latest_attempt_responses(student_id: int, quiz_id: int) -> tuple[dict[int, int], dict[str, Any] | None]:
    latest_attempt = get_latest_quiz_attempt(student_id, quiz_id)
    if not latest_attempt:
        return {}, None
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT question_id, selected_option_id
            FROM quiz_responses
            WHERE attempt_id = ?
            """,
            (latest_attempt["id"],),
        ).fetchall()
    mapping = {int(r["question_id"]): int(r["selected_option_id"]) for r in rows if r["selected_option_id"] is not None}
    return mapping, latest_attempt


def status_pill(module_row: dict[str, Any], unlocked: bool) -> tuple[str, str]:
    status = module_row.get("status")
    if status == "completed":
        return "Concluído", "pill pill-green"
    if not unlocked:
        return "Bloqueado", "pill pill-slate"
    if status == "in_progress":
        return "Em progresso", "pill pill-amber"
    return "Disponível", "pill pill-blue"


def fig_progress_donut(completion_rate: float) -> go.Figure:
    color = "#16a34a" if completion_rate >= 80 else "#2563eb"

    fig = go.Figure(
        data=[
            go.Pie(
                values=[completion_rate, max(0, 100 - completion_rate)],
                hole=0.74,
                textinfo="none",
                sort=False,
                marker=dict(
                    colors=[color, "#e2e8f0"],
                    line=dict(color="#ffffff", width=3),
                ),
                hoverinfo="skip",
            )
        ]
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        height=260,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[
            dict(
                text=f"<b>{completion_rate:.0f}%</b>",
                x=0.5,
                y=0.54,
                showarrow=False,
                font=dict(
                    size=34,
                    color="#0f172a",
                    family="Arial, sans-serif",
                ),
            ),
            dict(
                text="Conclusão",
                x=0.5,
                y=0.34,
                showarrow=False,
                font=dict(
                    size=14,
                    color="#64748b",
                    family="Arial, sans-serif",
                ),
            ),
        ],
    )

    return fig


def fig_module_scores(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["title"],
            y=df["score_pct"],
            marker=dict(
                color="#2563eb",
                line=dict(color="#1e3a8a", width=1),
            ),
            text=[f"{v:.0f}%" for v in df["score_pct"]],
            textposition="outside",  # 👈 MOSTRA OS VALORES
            textfont=dict(
                size=12,
                color="#0f172a"
            ),
            hovertemplate="%{y:.1f}%<extra></extra>",
        )
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=40),
        height=260,
        yaxis=dict(
            title="Score (%)",
            range=[0, 100],
            gridcolor="#e2e8f0",
        ),
        xaxis=dict(
            tickangle=-20,
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )

    return fig


def fig_teacher_modules(df: pd.DataFrame) -> go.Figure:
    fig = px.bar(df, x="module_title", y="avg_score_pct", text="avg_score_pct")
    fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="",
        yaxis_title="Média quiz (%)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,.55)",
    )
    return fig


def fig_teacher_students(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter(df, x="completion_rate", y="avg_score_pct", size="total_points", hover_name="full_name")
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Conclusão (%)",
        yaxis_title="Score médio (%)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,.55)",
    )
    return fig


def render_student_home() -> None:
    student_id = st.session_state.student_id
    course_id = st.session_state.course_id
    student = get_student(student_id)
    course = get_course(course_id)
    dashboard = get_student_dashboard(student_id, course_id)

    render_hero(
        f"{student['full_name']} · percurso de aprendizagem",
        f"{course['title']} — progressão estruturada, avaliação formativa e apoio à autorregulação.",
        tag="Estudante",
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Módulos concluídos", f"{dashboard['completed_modules']}/{dashboard['total_modules']}", "Progresso no percurso")
    with c2:
        render_metric_card("Taxa de conclusão", f"{dashboard['completion_rate']:.1f}%", "Ritmo de progressão")
    with c3:
        render_metric_card("Score médio", f"{dashboard['avg_score']:.1f}%", "Baseado nos miniquizzes")
    with c4:
        render_metric_card("Pontos", str(dashboard['total_points']), "Gamificação pedagógica")

    left, right = st.columns([1.05, 1.5], gap="large")
    with left:
        st.markdown("<div class='section-title'>Visão de progresso</div>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.plotly_chart(fig_progress_donut(dashboard["completion_rate"]), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>Badges</div>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        if dashboard["badges"]:
            html = "".join(
                f"<span class='badge-chip'>{b.get('icon') or '🏅'} {b['name']}</span>" for b in dashboard["badges"]
            )
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.info("Ainda sem badges. Conclui o primeiro módulo para iniciar o percurso gamificado.")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='section-title'>Desempenho por módulo</div>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        modules_df = pd.DataFrame(dashboard["modules"])
        if not modules_df.empty:
            modules_df["score_pct"] = modules_df["score"].fillna(0)
            st.plotly_chart(fig_module_scores(modules_df[["title", "score_pct"]]), use_container_width=True)
        else:
            st.info("Sem dados de módulos.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Percurso modular</div>", unsafe_allow_html=True)
    for module in dashboard["modules"]:
        unlocked = is_module_unlocked(student_id, module["module_id"])
        pill_label, pill_class = status_pill(module, unlocked)
        quiz = get_full_quiz(module["module_id"])
        quiz_count = len(quiz["questions"]) if quiz else 0
        score_pct = module.get("score")
        completion_pct = module.get("completion_rate") or 0
        required_pct = normalize_pct(module.get("passing_score")) or 60.0

        col1, col2 = st.columns([5.3, 1.2])
        with col1:
            st.markdown(
                f"""
                <div class="module-card">
                    <div class="module-title">Módulo {module['module_order']} — {module['title']}</div>
                    <div class="module-desc">{module.get('description') or 'Sem descrição disponível.'}</div>
                    <span class="{pill_class}">{pill_label}</span>
                    <span class="pill pill-blue">Quiz: {quiz_count} perguntas</span>
                    <span class="pill pill-rose">Meta: {required_pct:.0f}%</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            m1, m2, m3 = st.columns(3)
            m1.metric("Conclusão", f"{completion_pct:.0f}%")
            m2.metric("Melhor quiz", f"{score_pct:.0f}%" if score_pct is not None else "—")
            m3.metric("Desbloqueio", "Aberto" if unlocked else "Dependente")
        with col2:
            if unlocked:
                if st.button("Abrir módulo", key=f"open_{module['module_id']}", use_container_width=True, type="primary"):
                    st.session_state.module_id = module["module_id"]
                    st.session_state.page = "module_detail"
                    st.rerun()
            else:
                st.button("Bloqueado", key=f"lock_{module['module_id']}", disabled=True, use_container_width=True)


def render_module_detail() -> None:
    student_id = st.session_state.student_id
    module_id = st.session_state.module_id
    module = get_module(module_id)
    if not module:
        st.error("Módulo não encontrado.")
        return
    if not is_module_unlocked(student_id, module_id):
        st.warning("Este módulo ainda está bloqueado. Conclui primeiro o módulo anterior.")
        return

    mark_module_accessed(student_id, module_id)
    required_pct = normalize_pct(module.get("passing_score")) or 60.0
    feedback_summary = get_feedback_summary(module_id)

    top1, top2 = st.columns([5, 1])
    with top1:
        render_hero(
            f"Módulo {module['module_order']} — {module['title']}",
            "Exploração orientada, avaliação formativa, feedback imediato e integração com tutor RAG.",
            tag="Módulo",
        )
    with top2:
        st.write("")
        if st.button("⬅ Voltar", use_container_width=True):
            st.session_state.page = "student_home"
            st.rerun()

    i1, i2, i3 = st.columns(3)
    i1.metric("Score de aprovação", f"{required_pct:.0f}%")
    i2.metric("Clareza média", f"{(feedback_summary['avg_clarity'] or 0):.1f}/5")
    i3.metric("Utilidade média", f"{(feedback_summary['avg_usefulness'] or 0):.1f}/5")

    left, right = st.columns([1.55, 1], gap="large")
    with left:
        st.markdown("<div class='section-title'>Objetivos de aprendizagem</div>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        objectives = module.get("learning_objectives_list") or parse_json_list(module.get("learning_objectives"))
        if objectives:
            for item in objectives:
                st.markdown(f"- {item}")
        else:
            st.write(module.get("learning_objectives") or "Compreender os conceitos centrais do módulo e aplicá-los em contexto online assíncrono.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>Atividades sugeridas</div>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        activities = module.get("suggested_activities_list") or parse_json_list(module.get("suggested_activities"))
        if activities:
            for item in activities:
                st.markdown(f"- {item}")
        else:
            st.write(module.get("suggested_activities") or "Estudo dos materiais, resolução do miniquiz e consolidação com tutor RAG.")
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🤖 Abrir tutor RAG", use_container_width=False):
            log_rag_interaction(
                student_id,
                module_id,
                "Acesso ao tutor RAG",
                opened_from_analytics=True
            )
            st.session_state.page = "rag"
            st.session_state.rag_module_id = module_id  # opcional (muito útil 👇)
            st.rerun()

        render_quiz(student_id, module_id, required_pct)

    with right:
        render_material_feedback_box(student_id, module_id)


def render_quiz(student_id: int, module_id: int, required_pct: float) -> None:
    quiz = get_full_quiz(module_id)
    st.markdown("<div class='section-title'>Miniquiz formativo</div>", unsafe_allow_html=True)
    if not quiz:
        st.info("Este módulo ainda não tem miniquiz associado.")
        return

    latest_answers, latest_attempt = get_latest_attempt_responses(student_id, quiz["id"])
    if latest_attempt and latest_attempt.get("submitted_at"):
        last_score = normalize_pct(latest_attempt.get("score_pct")) or 0.0
        st.info(
            f"Última tentativa: #{latest_attempt.get('attempt_number', '—')} · {last_score:.0f}% · podes rever as respostas e submeter nova tentativa."
        )
    else:
        st.caption("Responde ao miniquiz para obter feedback imediato e atualizar o teu progresso.")

    feedback_key = f"quiz_feedback_{module_id}"
    if feedback_key in st.session_state:
        payload = st.session_state[feedback_key]
        if payload.get("score_pct") is not None:
            if payload.get("passed"):
                st.success(f"Excelente. Obtiveste {payload['score_pct']:.0f}% e concluíste o módulo.")
            else:
                st.warning(f"Obtiveste {payload['score_pct']:.0f}%. A meta para concluir este módulo é {required_pct:.0f}%.")
        st.markdown("### Feedback imediato")
        for item in payload.get("cards", []):
            if item["is_correct"]:
                st.success(f"**{item['question']}**\n\n{item['feedback']}")
            else:
                st.error(f"**{item['question']}**\n\n{item['feedback']}")

    with st.form(f"quiz_form_{module_id}"):
        answers: dict[int, int | None] = {}
        for question in quiz["questions"]:
            st.markdown(f"**{question['question_order']}. {question['question_text']}**")
            options = question["options"]
            option_texts = [opt["option_text"] for opt in options]
            option_ids = [int(opt["id"]) for opt in options]

            preselected_id = latest_answers.get(int(question["id"]))
            selected_index = option_ids.index(preselected_id) if preselected_id in option_ids else None
            selected = st.radio(
                label=f"Pergunta {question['id']}",
                options=option_texts,
                index=selected_index,
                key=f"quiz_{module_id}_{question['id']}",
                label_visibility="collapsed",
            )
            answers[int(question["id"])] = option_ids[option_texts.index(selected)] if selected is not None else None
            st.markdown("---")

        submitted = st.form_submit_button("Submeter miniquiz", use_container_width=True, type="primary")

    if submitted:
        if any(value is None for value in answers.values()):
            st.error("Responde a todas as perguntas antes de submeter.")
            return

        attempt_id = create_quiz_attempt(student_id, quiz["id"])
        total = len(quiz["questions"])
        correct_count = 0
        feedback_cards: list[dict[str, Any]] = []

        for question in quiz["questions"]:
            question_id = int(question["id"])
            selected_option_id = answers[question_id]
            assert selected_option_id is not None
            option_lookup = {int(opt["id"]): opt for opt in question["options"]}
            selected_option = option_lookup[selected_option_id]
            is_correct = bool(selected_option["is_correct"])
            feedback = selected_option.get("feedback_text") or (
                "Resposta correta." if is_correct else "Revê os conceitos principais deste tópico."
            )
            save_quiz_response(
                attempt_id=attempt_id,
                question_id=question_id,
                selected_option_id=selected_option_id,
                is_correct=is_correct,
                feedback=feedback,
                score_awarded=1.0 if is_correct else 0.0,
            )
            correct_count += int(is_correct)
            feedback_cards.append({
                "question": question["question_text"],
                "is_correct": is_correct,
                "feedback": feedback,
            })

        score_pct = round((correct_count / total) * 100, 2)
        finalize_quiz_attempt(attempt_id, score_pct)
        passed = complete_module_if_passed(student_id, module_id, required_pct)
        assign_basic_badges(student_id)

        st.session_state[feedback_key] = {
            "score_pct": score_pct,
            "passed": passed,
            "cards": feedback_cards,
        }
        st.rerun()

def render_material_feedback_box(student_id: int, module_id: int) -> None:
    st.markdown("<div class='section-title'>Avaliação dos materiais</div>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    existing = get_material_feedback(student_id, module_id)

    clarity_value = existing.get("clarity_rating") if existing else None
    usefulness_value = existing.get("usefulness_rating") if existing else None
    difficulty_value = existing.get("difficulty_rating") if existing else None
    comment_value = existing.get("comment") if existing else ""

    options = [1, 2, 3, 4, 5]

    def idx(v):
        return options.index(v) if v in options else None

    with st.form(f"feedback_form_{module_id}"):
        st.caption("Avalia os materiais do módulo. Podes atualizar a tua resposta a qualquer momento.")

        clarity = st.radio(
            "Clareza",
            options=options,
            index=idx(clarity_value),
            horizontal=True,
            key=f"clarity_{module_id}",
        )

        usefulness = st.radio(
            "Utilidade",
            options=options,
            index=idx(usefulness_value),
            horizontal=True,
            key=f"usefulness_{module_id}",
        )

        difficulty = st.radio(
            "Dificuldade percebida",
            options=options,
            index=idx(difficulty_value),
            horizontal=True,
            key=f"difficulty_{module_id}",
        )

        comment = st.text_area(
            "Comentário",
            value=comment_value or "",
            placeholder="O que foi mais útil? O que pode melhorar?",
            key=f"comment_{module_id}",
        )

        submitted = st.form_submit_button("Guardar avaliação", use_container_width=True)

    if submitted:
        if clarity is None or usefulness is None or difficulty is None:
            st.error("Seleciona clareza, utilidade e dificuldade percebida antes de guardar.")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        save_material_feedback(
            student_id,
            module_id,
            clarity,
            usefulness,
            comment.strip() or None,
            difficulty,
        )
        assign_basic_badges(student_id)
        st.success("Avaliação guardada com sucesso.")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

def get_teacher_student_detail(student_id: int, course_id: int) -> dict[str, Any]:
    student = get_student(student_id)
    dashboard = get_student_dashboard(student_id, course_id)
    reflections = fetch_all(
        """
        SELECT *
        FROM study_reflections
        WHERE student_id = ?
        ORDER BY COALESCE(updated_at, created_at) DESC
        LIMIT 5
        """,
        (student_id,),
    )
    rag_usage = fetch_one(
        """
        SELECT COUNT(*) AS cnt
        FROM rag_interactions
        WHERE student_id = ?
        """,
        (student_id,),
    )
    latest_feedback = fetch_all(
        """
        SELECT mf.*, m.title AS module_title
        FROM material_feedback mf
        JOIN modules m ON m.id = mf.module_id
        WHERE mf.student_id = ?
        ORDER BY mf.created_at DESC
        LIMIT 5
        """,
        (student_id,),
    )

    latest_activity = fetch_one(
        """
        SELECT MAX(last_activity_at) AS last_activity
        FROM module_progress
        WHERE student_id = ?
        """,
        (student_id,),
    )

    return {
        "student": student,
        "dashboard": dashboard,
        "reflections": reflections,
        "rag_count": int(rag_usage["cnt"]) if rag_usage else 0,
        "latest_feedback": latest_feedback,
        "last_activity": latest_activity["last_activity"] if latest_activity else None,
    }


def build_gamification_ranking(course_id: int) -> pd.DataFrame:
    students = get_users_by_role("student")
    rows = []

    for student in students:
        dash = get_student_dashboard(student["id"], course_id)
        rows.append(
            {
                "student_id": student["id"],
                "full_name": student["full_name"],
                "points": dash["total_points"],
                "badges": len(dash["badges"]),
                "completed_modules": dash["completed_modules"],
                "completion_rate": dash["completion_rate"],
                "avg_score": dash["avg_score"],
            }
        )

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df = df.sort_values(
        by=["points", "completed_modules", "avg_score", "completion_rate"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)
    df.insert(0, "rank", df.index + 1)
    return df


def build_attention_list(course_id: int) -> pd.DataFrame:
    students = get_users_by_role("student")
    rows = []

    for student in students:
        dash = get_student_dashboard(student["id"], course_id)
        last_activity_row = fetch_one(
            """
            SELECT MAX(last_activity_at) AS last_activity
            FROM module_progress
            WHERE student_id = ?
            """,
            (student["id"],),
        )
        rows.append(
            {
                "student_id": student["id"],
                "full_name": student["full_name"],
                "completion_rate": dash["completion_rate"],
                "avg_score": dash["avg_score"],
                "points": dash["total_points"],
                "badges": len(dash["badges"]),
                "last_activity": last_activity_row["last_activity"] if last_activity_row else None,
            }
        )

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df = df.sort_values(
        by=["completion_rate", "avg_score", "points"],
        ascending=[True, True, True],
    ).reset_index(drop=True)
    return df.head(5)


def fig_gamification_ranking(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return go.Figure()

    fig = go.Figure(
        data=[
            go.Bar(
                x=df["points"],
                y=df["full_name"],
                orientation="h",
                text=[f"{p} pts" for p in df["points"]],
                textposition="outside",
                marker=dict(
                    color="#2563eb",
                    line=dict(color="#1e3a8a", width=1),
                ),
                hovertemplate="<b>%{y}</b><br>%{x} pontos<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        height=380,
        margin=dict(l=180, r=30, t=10, b=20),
        xaxis_title="Pontos",
        yaxis_title="",
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(size=13, color="#0f172a"),
            automargin=True,
        ),
        xaxis=dict(
            tickfont=dict(size=12, color="#0f172a"),
            gridcolor="#e2e8f0",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,.55)",
        showlegend=False,
    )
    return fig

def fig_student_module_progress(modules_df: pd.DataFrame) -> go.Figure:
    if modules_df.empty:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=modules_df["title"],
            y=modules_df["completion_rate"],
            name="Conclusão",
            marker=dict(color="#93c5fd"),
            text=[f"{v:.0f}%" for v in modules_df["completion_rate"]],
            textposition="inside",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=modules_df["title"],
            y=modules_df["score"].fillna(0),
            mode="lines+markers+text",
            name="Quiz",
            text=[f"{v:.0f}%" if pd.notna(v) else "—" for v in modules_df["score"]],
            textposition="top center",
            line=dict(color="#1d4ed8", width=3),
            marker=dict(size=8),
        )
    )

    fig.update_layout(
        height=340,
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis_title="Percentagem",
        xaxis_title="",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,.55)",
        legend=dict(orientation="h", y=1.1, x=0),
    )

    return fig

def render_teacher_home() -> None:
    course_id = st.session_state.course_id
    course = get_course(course_id)

    render_hero(
        "Dashboard docente",
        f"{course['title']} — acompanhamento pedagógico, progressão, gamificação e apoio à decisão.",
        tag="Professor",
    )

    module_rows = get_teacher_module_overview()
    module_rows = [m for m in module_rows if m.get("course_id") == course_id] if module_rows else []

    all_students = get_users_by_role("student")
    ranking_df = build_gamification_ranking(course_id)
    attention_df = build_attention_list(course_id)

    avg_completion = float(ranking_df["completion_rate"].mean()) if not ranking_df.empty else 0.0
    avg_score = float(ranking_df["avg_score"].mean()) if not ranking_df.empty else 0.0
    avg_points = float(ranking_df["points"].mean()) if not ranking_df.empty else 0.0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Estudantes", str(len(all_students)), "Turma acompanhada")
    with c2:
        render_metric_card("Conclusão média", f"{avg_completion:.1f}%", "Progressão global")
    with c3:
        render_metric_card("Score médio", f"{avg_score:.1f}%", "Desempenho formativo")
    with c4:
        render_metric_card("Pontos médios", f"{avg_points:.0f}", "Envolvimento gamificado")

    top_left, top_right = st.columns([1.25, 1], gap="large")

    with top_left:
        st.markdown("<div class='section-title'>Gamificação da turma</div>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        if not ranking_df.empty:
            st.plotly_chart(
                fig_gamification_ranking(ranking_df.head(8)),
                use_container_width=True,
            )
        else:
            st.info("Sem dados de gamificação.")
        st.markdown("</div>", unsafe_allow_html=True)

    with top_right:
        st.markdown("<div class='section-title'>Estudantes a necessitar de apoio</div>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        if not attention_df.empty:
            for _, row in attention_df.iterrows():
                st.markdown(
                    f"""
                    <div style="
                        padding: .8rem .9rem;
                        border-radius: 16px;
                        background: rgba(255,255,255,.72);
                        border: 1px solid rgba(148,163,184,.15);
                        margin-bottom: .7rem;
                    ">
                        <div style="font-weight: 800; color: #0f172a;">{row['full_name']}</div>
                        <div style="font-size: .9rem; color: #475569;">
                            Conclusão: {row['completion_rate']:.1f}% ·
                            Score: {row['avg_score']:.1f}% ·
                            Pontos: {row['points']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("Sem estudantes sinalizados.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Análise individual do estudante</div>", unsafe_allow_html=True)

    if not all_students:
        st.info("Sem estudantes disponíveis.")
        return

    student_options = {s["full_name"]: s["id"] for s in all_students}
    selected_student_name = st.selectbox(
        "Selecionar estudante",
        options=list(student_options.keys()),
        key="teacher_selected_student",
    )
    selected_student_id = student_options[selected_student_name]

    detail = get_teacher_student_detail(selected_student_id, course_id)
    student_dash = detail["dashboard"]
    student_modules_df = pd.DataFrame(student_dash["modules"])

    if not student_modules_df.empty:
        if "score" not in student_modules_df.columns:
            student_modules_df["score"] = student_modules_df.get("best_quiz_score_pct", 0)
        if "completion_rate" not in student_modules_df.columns:
            student_modules_df["completion_rate"] = student_modules_df.get("completion_pct", 0)

    d1, d2, d3, d4, d5 = st.columns(5)
    with d1:
        render_metric_card("Módulos concluídos", f"{student_dash['completed_modules']}/{student_dash['total_modules']}")
    with d2:
        render_metric_card("Conclusão", f"{student_dash['completion_rate']:.1f}%")
    with d3:
        render_metric_card("Score médio", f"{student_dash['avg_score']:.1f}%")
    with d4:
        render_metric_card("Pontos", str(student_dash["total_points"]))
    with d5:
        render_metric_card("Badges", str(len(student_dash["badges"])), "Reconhecimento formativo")

    lower_left, lower_right = st.columns([1.45, 1], gap="large")

    with lower_left:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### Progresso por módulo")
        if not student_modules_df.empty:
            st.plotly_chart(fig_student_module_progress(student_modules_df), use_container_width=True)
        else:
            st.info("Sem dados de módulos para este estudante.")
        st.markdown("</div>", unsafe_allow_html=True)

    with lower_right:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### Perfil de envolvimento")
        st.write(f"**Estudante:** {detail['student']['full_name']}")
        st.write(f"**Última atividade:** {detail['last_activity'] or '—'}")
        st.write(f"**Feedback submetido:** {len(detail['latest_feedback'])}")
        st.write(f"**Reflexões registadas:** {len(detail['reflections'])}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### Badges conquistados")
        if student_dash["badges"]:
            html = "".join(
                f"<span class='badge-chip'>{b.get('icon') or '🏅'} {b['name']}</span>"
                for b in student_dash["badges"]
            )
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.info("Sem badges atribuídos.")
        st.markdown("</div>", unsafe_allow_html=True)

    bottom_left, bottom_right = st.columns(2, gap="large")

    with bottom_left:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### Feedback sobre materiais")
        if detail["latest_feedback"]:
            for item in detail["latest_feedback"]:
                st.markdown(
                    f"""
                    **{item['module_title']}**  
                    Clareza: {item.get('clarity_rating', '—')}/5 ·
                    Utilidade: {item.get('usefulness_rating', '—')}/5  
                    {item.get('comment') or '_Sem comentário._'}
                    """
                )
                st.markdown("---")
        else:
            st.info("Sem feedback registado.")
        st.markdown("</div>", unsafe_allow_html=True)

    with bottom_right:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### Reflexões recentes")
        if detail["reflections"]:
            for item in detail["reflections"]:
                learned = item.get("learned_text") or "—"
                difficulties = item.get("difficulties_text") or "—"
                next_steps = item.get("next_steps_text") or "—"
                st.markdown(
                    f"""
                    **Aprendido:** {learned}  
                    **Dificuldades:** {difficulties}  
                    **Próximos passos:** {next_steps}
                    """
                )
                st.markdown("---")
        else:
            st.info("Sem reflexões registadas.")
        st.markdown("</div>", unsafe_allow_html=True)

def get_material_feedback(student_id: int, module_id: int) -> dict[str, Any] | None:
    return fetch_one(
        """
        SELECT *
        FROM material_feedback
        WHERE student_id = ? AND module_id = ?
        """,
        (student_id, module_id),
    )        

def main() -> None:
    inject_css()
    init_state()
    if not st.session_state.authenticated:
        render_login()
        return

    render_sidebar()

    if st.session_state.page == "rag":
        render_rag_page()

    elif st.session_state.role == "Professor":
        render_teacher_home()

    else:
        if st.session_state.page == "module_detail" and st.session_state.module_id is not None:
            render_module_detail()
        else:
            render_student_home()

if __name__ == "__main__":
    main()
