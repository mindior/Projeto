from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

import streamlit as st

from src.load_pdfs import extract_pages
from src.chunking import chunk_pages
from src.embed_store import build_and_save_index
from src.rag_chain import answer_question


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
STORE_DIR = BASE_DIR / "vector_store"
SHOW_REINDEX = False

def render_rag_page():
    from .src.rag_chain import answer_question
    from pathlib import Path
    import streamlit as st

    BASE_DIR = Path(__file__).parent
    STORE_DIR = BASE_DIR / "vector_store"

    st.markdown("<div style='margin-top: 2.0rem;'></div>", unsafe_allow_html=True)

    top_left, top_right = st.columns([4, 1])

    with top_left:
        st.markdown("<div class='section-title'>Tutor inteligente (RAG)</div>", unsafe_allow_html=True)
        st.caption("Assistente baseado nos materiais da disciplina.")

    with top_right:
        if st.button("⬅ Voltar", use_container_width=True):
            st.session_state.page = "module_detail" if st.session_state.get("module_id") else "student_home"
            st.rerun()

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    c1, c2 = st.columns([1.2, 1])
    with c1:
        mode = st.selectbox("Modo de resposta", ["Simples", "Técnico", "Estudo"], index=0)
    with c2:
        top_k = st.slider("N.º de excertos", min_value=2, max_value=6, value=4)

    question = st.text_area(
        "Faça uma pergunta sobre os conteúdos",
        placeholder="Ex.: Explique interpretabilidade vs explicabilidade.",
        height=120,
    )

    if st.button("Perguntar", type="primary"):
        if not question.strip():
            st.warning("Escreva uma pergunta.")
        elif not (STORE_DIR / "index.faiss").exists():
            st.error("Índice vetorial não encontrado.")
        else:
            with st.spinner("A gerar resposta..."):
                result = answer_question(
                    question=question,
                    store_dir=STORE_DIR,
                    mode=mode,
                    top_k=top_k,
                )

            st.subheader("Resposta")
            st.write(result["answer"])

            st.subheader("Fontes")
            for i, src in enumerate(result["sources"], start=1):
                with st.expander(f"Fonte {i} — {src['source']} | pág. {src['page_number']}"):
                    st.write(src["text"][:800])

    st.markdown("</div>", unsafe_allow_html=True)