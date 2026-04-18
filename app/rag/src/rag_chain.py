from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List

import streamlit as st
from google import genai

from .retriever import search


MODEL_NAME = "gemini-2.5-flash"


STYLE_INSTRUCTIONS = {
    "Simples": "Responde em linguagem clara, acessível e didática.",
    "Técnico": "Responde com maior rigor técnico e terminologia especializada.",
    "Estudo": "Responde como tutor: explica passo a passo e destaca ideias-chave.",
}


def _client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("Defina a variável de ambiente GEMINI_API_KEY.")

    return genai.Client(api_key=api_key)


def detect_question_type(question: str) -> str:
    q = question.lower()

    if "o que é" in q or "defina" in q or "define" in q:
        return "definicao"

    return "geral"


def build_context(retrieved: List[Dict]) -> str:
    blocks = []

    for i, item in enumerate(retrieved, start=1):
        book_name = "LLM" if "llm" in item["source"].lower() else "XAI"

        snippet = item["text"][:900]

        blocks.append(
            f"[Fonte {i}] Livro: {book_name} ({item['source']}) | Página: {item['page_number']} | "
            f"Score: {item['score']:.3f}\n{snippet}"
        )

    return "\n\n".join(blocks)


def answer_question(
    question: str,
    store_dir: Path,
    mode: str = "Simples",
    top_k: int = 4,
) -> Dict:

    retrieved = search(question, store_dir=store_dir, top_k=top_k)

    # 🔹 Sem contexto
    if not retrieved:
        return {
            "answer": "Não encontrei informação suficiente nos textos para responder com segurança.",
            "sources": []
        }

    # 🔹 Métricas de confiança
    max_score = max(r["score"] for r in retrieved)
    avg_score = sum(r["score"] for r in retrieved) / len(retrieved)

    # 🔥 Detecção fora de domínio (ajustada)
    if max_score < 0.25 and avg_score < 0.22:
        return {
            "answer": "A pergunta está fora do âmbito dos materiais da disciplina. Este sistema responde apenas com base nos conteúdos dos livros fornecidos.",
            "sources": []
        }

    context = build_context(retrieved)

    question_type = detect_question_type(question)

    # 🔹 Instrução adaptativa
    if question_type == "definicao":
        extra_instruction = """
A pergunta pede uma definição.

Começa com uma definição clara e direta em uma frase.
Depois desenvolve com base no contexto.
Se a definição não estiver explícita no texto, indica isso e constrói uma definição coerente com o contexto.
"""
    else:
        extra_instruction = ""

    system_prompt = f"""
És um assistente pedagógico especializado em conteúdos académicos.

{STYLE_INSTRUCTIONS.get(mode, STYLE_INSTRUCTIONS["Simples"])}

Regras fundamentais:

1. Usa PRINCIPALMENTE o contexto fornecido.
2. NÃO inventes informação fora do texto.
3. Se a pergunta estiver fora do conteúdo, deves recusar responder.
4. Podes complementar apenas se for coerente com o contexto.
5. Se a informação for limitada, indica isso claramente.
6. Prefere explicações claras e pedagógicas.
7. Evita repetir texto — usa paráfrases.
8. Indica se o conteúdo é mais relacionado com LLM ou XAI.

{extra_instruction}

Se a resposta não estiver totalmente suportada pelo contexto, deves indicar explicitamente essa limitação.

No final inclui:
"Base da resposta:" com referência às fontes utilizadas.
"""

    user_prompt = f"""Pergunta do estudante:
{question}

Contexto recuperado:
{context}

Produz uma resposta clara, estruturada e fiel ao contexto.
"""

    client = _client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_prompt,
        config={
            "system_instruction": system_prompt,
            "temperature": 0.2,
        },
    )

    answer_text = getattr(response, "text", "") or "Não foi possível gerar resposta."

    return {
        "answer": answer_text,
        "sources": retrieved
    }