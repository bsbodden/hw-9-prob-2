import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader
from loadllm import load_llama2_model
from streamlit_chat import message
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Redis
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import HuggingFacePipeline
import time
import redis
import tempfile

REDIS_URL = "redis://localhost:6379"

class FileIngestorLLM:
    def __init__(self, uploaded_file):
        self.uploaded_file = uploaded_file
        self.total_time = 0
        self.tokens_processed = 0
        self.llm = load_llama2_model()

    def handle_file_and_ingest_llm(self):
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(self.uploaded_file.read())
            tmp_file_path = tmp_file.name

        loader = PyMuPDFLoader(file_path=tmp_file_path)
        data = loader.load()

        # Create embeddings using Sentence Transformers
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

        # Create a Redis client
        redis_client = redis.from_url(REDIS_URL)

        # Create a Redis vector store and save embeddings
        db = Redis.from_documents(
            data,
            embeddings,
            redis_url=REDIS_URL,
            index_name="pdf_index"
        )

        # Create a conversational chain
        chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=db.as_retriever()
        )

        # Function for conversational chat
        def conversational_chat(query):
            start_time = time.time()
            if isinstance(query, list):
                query = query[0]
            result = chain({"question": query, "chat_history": st.session_state['history']})
            end_time = time.time()
            self.total_time += end_time - start_time

            # Calculate the number of tokens processed
            prompt_tokens = self.llm.get_num_tokens(query)
            completion_tokens = self.llm.get_num_tokens(result["answer"])
            self.tokens_processed += prompt_tokens + completion_tokens

            st.session_state['history'].append((query, result["answer"]))
            return result["answer"]

        # Initialize chat history
        if 'history' not in st.session_state:
            st.session_state['history'] = []

        # Initialize messages
        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Hello! Ask me about the PDF uploaded 🤗"]

        if 'past' not in st.session_state:
            st.session_state['past'] = ["Hey! 👋"]

        # Create containers for chat history and user input
        response_container = st.container()
        container = st.container()

        # User input form
        with container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input("Query:", placeholder="Talk to PDF data 🧮", key='input')
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                output = conversational_chat(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

        # Display chat history
        if st.session_state['generated']:
            with response_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                    message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")