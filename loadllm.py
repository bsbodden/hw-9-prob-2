from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
import streamlit as st

@st.cache_resource
def load_llama2_model():
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    model = Ollama(model="gemma:2b")

    return model