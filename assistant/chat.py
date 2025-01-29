import asyncio
import logging
import streamlit as st
from utils.common import apply_nest_asyncio, configure_logging, load_environment_variables
from stockbroker import run_command

configure_logging(level=logging.DEBUG)
apply_nest_asyncio()
load_environment_variables()

with st.sidebar:
    options = ["Llama3.1", "Deepseek-r1:8b", "Llama3.2:3b-instruct-fp16"]
    llm_model = st.selectbox("Available models", options)

st.title("💬 Alfred")
st.caption("🚀 Your smart bulter, at your service ...")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    output = asyncio.run(run_command(prompt, True, llm_model.lower()))
    st.session_state.messages.append({"role": "assistant", "content": output})
    st.chat_message("assistant").write(output)