"""
app.py — PSX Investment Agent: Multi-Model Chat via OpenRouter
Run with: streamlit run app.py
"""

import os

import streamlit as st
from dotenv import load_dotenv

from openrouter_client import OpenRouterClient
from skill_loader import load_skills

load_dotenv()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SKILLS_DIR = os.path.dirname(os.path.abspath(__file__))

MODELS: dict[str, dict[str, str]] = {
    "Anthropic": {
        "Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet",
        "Claude 3 Opus": "anthropic/claude-3-opus",
    },
    "Google": {
        "Gemini 1.5 Pro": "google/gemini-pro-1.5",
        "Gemini 1.5 Flash": "google/gemini-flash-1.5",
    },
    "Open Source": {
        "Llama 3.1 70B": "meta-llama/llama-3.1-70b-instruct",
        "Mistral Large": "mistralai/mistral-large",
        "DeepSeek Chat": "deepseek/deepseek-chat",
    },
}

# ---------------------------------------------------------------------------
# Cached skill loading (reads ZIPs only once per server process)
# ---------------------------------------------------------------------------
@st.cache_resource
def _load_skills_cached(skills_dir: str) -> dict:
    return load_skills(skills_dir)


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="PSX Investment Agent",
    page_icon="📈",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
skills = _load_skills_cached(SKILLS_DIR)

if "messages" not in st.session_state:
    st.session_state.messages: list[dict] = []

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Settings")

    # API Key
    api_key = st.text_input(
        "OpenRouter API Key",
        value=os.getenv("OPENROUTER_API_KEY", ""),
        type="password",
        placeholder="sk-or-...",
        help="Get your key at https://openrouter.ai/keys",
    )

    st.divider()

    # Provider → Model selection
    st.subheader("Model")
    provider = st.selectbox("Provider", list(MODELS.keys()))
    model_name = st.selectbox("Model", list(MODELS[provider].keys()))
    model_id = MODELS[provider][model_name]

    st.divider()

    # Skill selection
    st.subheader("Skill (System Prompt)")
    skill_names = list(skills.keys())

    if skill_names:
        selected_skill = st.selectbox("Active Skill", skill_names)
        skill_info = skills[selected_skill]

        include_refs = st.checkbox(
            "Include reference documents",
            value=True,
            help="Append embedded reference docs to the system prompt. "
                 "Disable for smaller models with limited context.",
        )
        if skill_info["reference_files"]:
            st.caption(
                f"📎 {len(skill_info['reference_files'])} reference doc(s): "
                + ", ".join(skill_info["reference_files"])
            )

        system_prompt = (
            skill_info["system_prompt"]
            if include_refs
            else skill_info["system_prompt_skill_only"]
        )
        with st.expander("Preview system prompt"):
            st.markdown(f"```\n{system_prompt[:800]}…\n```")
    else:
        selected_skill = None
        include_refs = False
        system_prompt = (
            "You are an expert PSX (Pakistan Stock Exchange) investment analyst. "
            "Provide detailed, data-driven investment analysis."
        )
        st.warning("No .skill files found — using default system prompt.")

    st.divider()

    # Temperature
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.05)

    st.divider()

    # Clear chat
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------------------------------------------------
# Main area — header
# ---------------------------------------------------------------------------
st.title("📈 PSX Investment Agent")

col1, col2 = st.columns(2)
with col1:
    st.caption(f"**Model:** {provider} / {model_name} (`{model_id}`)")
with col2:
    if selected_skill:
        st.caption(f"**Skill:** {selected_skill}")

st.divider()

# ---------------------------------------------------------------------------
# Chat history
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------
if not api_key:
    st.warning("Enter your OpenRouter API key in the sidebar to start chatting.")
    st.stop()

user_input = st.chat_input("Ask about PSX stocks, sectors, portfolio, valuations…")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Build messages for API call (system prompt + full history)
    api_messages = [{"role": "system", "content": system_prompt}] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    # Stream assistant response
    with st.chat_message("assistant"):
        try:
            client = OpenRouterClient(api_key=api_key)

            def _token_stream():
                yield from client.stream_chat(model_id, api_messages, temperature)

            full_response = st.write_stream(_token_stream())
        except Exception as exc:
            st.error(f"**Error:** {exc}")
            st.session_state.messages.pop()  # remove user message so they can retry
            st.stop()

    st.session_state.messages.append({"role": "assistant", "content": full_response})
