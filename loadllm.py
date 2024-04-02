from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import LlamaCpp
import streamlit as st

model_path = './llama-2-7b-chat.Q4_K_M.gguf'

@st.cache_resource
def load_llama2_model():
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    model = LlamaCpp(
        model_path=model_path,
        n_gpu_layers=40,
        n_batch=512,
        n_ctx=2048,
        f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
        callback_manager=callback_manager,
        verbose=True,
    )

    return model