import asyncio
import logging
import streamlit as st
from utils.common import apply_nest_asyncio, configure_logging, load_environment_variables
from stockbroker import run_command as run_stock_command
from travelassistant import run_command as run_travel_command
import requests

configure_logging(level=logging.DEBUG)
apply_nest_asyncio()
load_environment_variables()

def get_available_models():
    response = requests.get("http://localhost:11434/api/tags")
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()
    return [model["model"] for model in data.get("models", [])]


with st.sidebar:
    llm_model = st.selectbox("Available models", get_available_models())
    agents = st.selectbox("Select the agent", ["Financial broker", "Travel agent"])

st.title("💬 Alfred")
st.caption("🚀 Your smart bulter, at your service ...")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.status("Thinking ...", expanded=True) as status:
        st.chat_message("user").write(prompt)
        if agents == "Financial broker":
            output = asyncio.run(run_stock_command(prompt, True, llm_model.lower()))
        else:
            output = asyncio.run(run_travel_command(prompt, True, llm_model.lower()))
        status.update(label="Done thinking, answering ...", state="complete", expanded=True)
        st.session_state.messages.append({"role": "assistant", "content": output})
        st.chat_message("assistant").write(output)