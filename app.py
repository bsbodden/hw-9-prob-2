import streamlit as st
from fileingestor import FileIngestorLLM

# Set the title for the Streamlit app
st.title("Chat with PDF - 🤖 🔗")

# Create a file uploader in the sidebar
uploaded_file = st.sidebar.file_uploader("Upload File", type="pdf")

if uploaded_file is not None:
    # Process the file using the FileIngestorLLM class
    ingestor = FileIngestorLLM(uploaded_file)
    ingestor.handle_file_and_ingest_llm()

    # Display the total time and tokens processed
    st.sidebar.info(f"Total Time: {ingestor.total_time:.2f} seconds")
    st.sidebar.info(f"Tokens Processed: {ingestor.tokens_processed}")