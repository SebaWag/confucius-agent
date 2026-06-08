"""Confucius Agent — Streamlit Demo Interface.

Interactive demo showcasing hierarchical memory:
- Chat with the agent
- Inspect memory tiers
- Add/view Mental Models and Observations
- See priority-based retrieval in action
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from confucius.agent import ConfuciusAgent
from confucius.memory.retrieval_pipeline import RetrievalPipeline


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


st.title("🏛️ Confucius Agent")
st.markdown("*Hierarchical Memory for AI Agents on Qwen Cloud*")
st.markdown("---")

# Sidebar — Memory Inspector
with st.sidebar:
    st.header("🧠 Memory Inspector")
    st.caption("Query all 3 memory tiers and see priority ranking")

    mem_query = st.text_input("Search memory:", placeholder="e.g., project rules...")
    if st.button("🔍 Search") and mem_query:
        with st.spinner("Querying all tiers..."):
            results = st.session_state.pipeline.query(mem_query)
        
        st.subheader("Results by Tier")
        for tier, count in results["stats"].items():
            st.caption(f"{tier}: {count} items")
        
        st.subheader("Ranked Context")
        for item in results["context"]:
            tier_icons = {
                "mental_model": "🏛️",
                "observation": "📝",
                "raw_fact": "📦",
            }
            icon = tier_icons.get(item.get("tier", ""), "📄")
            rank = item.get("rank", 0)
            st.markdown(f"{icon} **[{item.get('tier', '?')}]** (rank: {rank:.2f})")
            st.caption(item["content"][:150] + "...")
            st.divider()

    st.divider()
    st.header("➕ Add Knowledge")
    
    with st.form("add_mental_model"):
        st.subheader("🏛️ Mental Model")
        content = st.text_area("Content:", placeholder="Company policy: ...")
        source = st.text_input("Source:", placeholder="onboarding docs")
        if st.form_submit_button("Add"):
            if content:
                st.session_state.pipeline.add_mental_model(content, source)
                st.success("✅ Mental Model stored!")
    
    with st.form("add_observation"):
        st.subheader("📝 Observation")
        obs_content = st.text_area("Observation:", placeholder="Learned that...")
        obs_cat = st.selectbox("Category", ["general", "code", "decision", "pattern"])
        if st.form_submit_button("Add"):
            if obs_content:
                st.session_state.pipeline.add_observation(obs_content, obs_cat)
                st.success("✅ Observation stored!")


# Main chat area
st.header("💬 Chat with Confucius Agent")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me anything — I remember across sessions..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🧠 Searching memory tiers..."):
            response = st.session_state.agent.process_message(prompt)
        st.markdown(response)
        st.caption("🤖 Context: Mental Models 🏛️ → Observations 📝 → Raw Facts 📦")
    
    st.session_state.messages.append({"role": "assistant", "content": response})
