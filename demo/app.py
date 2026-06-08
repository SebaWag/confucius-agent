"""Confucius Agent — Streamlit Demo Interface.

Interactive demo showcasing hierarchical memory:
- Chat with the agent
- Inspect memory tiers
- Upload documents to build Mental Models
- See priority-based retrieval in action
"""

import streamlit as st
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from confucius.agent import ConfuciusAgent
from confucius.memory.retrieval_pipeline import RetrievalPipeline
from confucius.ingester import DocumentIngester


st.set_page_config(
    page_title="Confucius Agent — Hierarchical Memory",
    page_icon="🏛️",
    layout="wide",
)

# Initialize
if "agent" not in st.session_state:
    st.session_state.agent = ConfuciusAgent()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pipeline" not in st.session_state:
    st.session_state.pipeline = RetrievalPipeline()
if "ingester" not in st.session_state:
    st.session_state.ingester = DocumentIngester()
if "ingestion_history" not in st.session_state:
    st.session_state.ingestion_history = []


st.title("🏛️ Confucius Agent")
st.markdown("*Hierarchical Memory for AI Agents on Qwen Cloud*")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📄 Cargar Documentos")
    st.caption(
        "Sube documentos de tu empresa para construir la "
        "**Memoria Canónica** del agente. "
        f"Formatos: {DocumentIngester.get_supported_formats()}"
    )

    uploaded_files = st.file_uploader(
        "Selecciona archivos",
        type=["txt", "md", "pdf", "csv", "json", "yaml", "yml", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded_files:
        progress_bar = st.progress(0, text="Preparando...")
        status_text = st.empty()
        results_container = st.container()

        total = len(uploaded_files)
        for i, uploaded_file in enumerate(uploaded_files):
            file_label = uploaded_file.name[:50] + "..." if len(uploaded_file.name) > 50 else uploaded_file.name
            status_text.info(f"📄 Procesando: {file_label}")

            result = st.session_state.ingester.ingest(
                uploaded_file.name,
                uploaded_file.getvalue(),
                source_label=f"upload: {uploaded_file.name}",
            )

            st.session_state.ingestion_history.append(result)

            with results_container:
                if result["success"]:
                    st.success(f"✅ **{uploaded_file.name}** — {result['chunks']} fragmentos almacenados como 🏛️ Mental Models")
                else:
                    st.error(f"❌ **{uploaded_file.name}** — {result['error']}")

            progress_bar.progress((i + 1) / total, text=f"{i+1}/{total} documentos procesados")
            time.sleep(0.3)

        progress_bar.empty()
        status_text.success(f"✅ {total} documentos procesados. El agente ya puede consultar esta información.")
        st.balloons()

    st.divider()

    # === Knowledge Base Stats ===
    st.header("📊 Estado de la Memoria")
    total_mm = len(st.session_state.ingestion_history)
    total_chunks = sum(r.get("chunks", 0) for r in st.session_state.ingestion_history if r.get("success"))
    st.metric("🏛️ Mental Models almacenados", total_chunks)
    st.metric("📄 Documentos procesados", total_mm)

    if st.session_state.ingestion_history:
        with st.expander("📋 Últimas ingestiones"):
            for r in st.session_state.ingestion_history[-5:]:
                if r["success"]:
                    st.caption(f"✅ {r['file']} → {r['chunks']} chunks")
                else:
                    st.caption(f"❌ {r.get('file', 'N/A')} → {r['error']}")

    st.divider()

    # === Memory Inspector ===
    st.header("🧠 Memory Inspector")
    st.caption("Busca en los 3 niveles de memoria")

    mem_query = st.text_input("Buscar en memoria:", placeholder="ej: políticas de la empresa...", key="mem_search")
    if st.button("🔍 Buscar") and mem_query:
        with st.spinner("Consultando todos los niveles..."):
            results = st.session_state.pipeline.query(mem_query)

        st.subheader("Resultados por nivel")
        for tier, count in results["stats"].items():
            tier_icons = {"mental_models": "🏛️", "observations": "📝", "raw_facts": "📦"}
            st.caption(f"{tier_icons.get(tier, '📄')} {tier}: {count} items")

        st.subheader("Contexto priorizado")
        for item in results["context"]:
            tier = item.get("tier", "?")
            tier_icons = {"mental_model": "🏛️", "observation": "📝", "raw_fact": "📦"}
            icon = tier_icons.get(tier, "📄")
            rank = item.get("rank", 0)
            st.markdown(f"{icon} **[{tier}]** (prioridad: {rank:.2f})")
            st.caption(item["content"][:200] + ("..." if len(item["content"]) > 200 else ""))
            st.divider()

    st.divider()

    # === Manual Knowledge Entry ===
    st.header("➕ Añadir Conocimiento Manual")
    with st.form("add_mental_model"):
        st.subheader("🏛️ Mental Model")
        content = st.text_area("Contenido:", placeholder="Política de la empresa: ...", height=100)
        source = st.text_input("Fuente:", placeholder="documento de onboarding")
        if st.form_submit_button("Guardar como Mental Model 🏛️"):
            if content:
                result = st.session_state.pipeline.add_mental_model(content, source or "manual")
                st.success(f"✅ Almacenado (id: {result})")

    with st.form("add_observation"):
        st.subheader("📝 Observation (aprendizaje)")
        obs_content = st.text_area("Observación:", placeholder="Aprendí que...", height=100)
        obs_cat = st.selectbox("Categoría", ["general", "code", "decision", "pattern", "preference"])
        if st.form_submit_button("Guardar como Observation 📝"):
            if obs_content:
                st.session_state.pipeline.add_observation(obs_content, obs_cat)
                st.success("✅ Observation almacenada")


# Main chat area
st.header("💬 Chatea con Confucius Agent")
st.caption("El agente consulta automáticamente los documentos que subiste — pruébalo preguntando sobre la información que cargaste.")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Pregúntame lo que sea — recuerdo entre sesiones..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🧠 Buscando en los 3 niveles de memoria..."):
            response = st.session_state.agent.process_message(prompt)
        st.markdown(response)
        st.caption("🤖 Memoria consultada: 🏛️ Mental Models → 📝 Observations → 📦 Raw Facts")

    st.session_state.messages.append({"role": "assistant", "content": response})
