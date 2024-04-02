### Problem 2

Please download the LLM model llama-2-7b-chat.Q4_K_M.gguf from huggingface.co and  implement the The “Chat with PDF” app as described in this article-
https://medium.com/@gaurav.jaik86/building-an-ai-powered-chat-with-pdf-app-with-streamlit-langchain-faiss-and-llama2-affadea65737
Download the Llama2 model from - https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf
Create 3 .py files as:
 - a. app.py -> To create app interface
 - b. loadllm.py -> To load the Llama2 model locally
 - c. fileingestor.py -> To upload PDF file and create chain for question answering

Run command "streamlit run app.py" -> This will run the app on http://localhost:8501
You will be able to upload any PDF file and run some query on the uploaded PDF
Capture the screenshot of the uploaded PDF and the query invoked and the response
Capture the total time it took to run the query and the tokens processed.
You can experiment with another model of your choice and change the model path in the loadllm.py file and run the streamlit app again with the same PDF file and the same query and report your findings.
(25%)

You'll need Poetry to manage dependencies and run the application. Once you install Poetry you can:

Install dependencies:

```bash
poetry install
```
Start Redis Stack with the provided Docker Compose YAML file for using [Redis Stack](https://redis.io/docs/stack/).

```bash
docker compose up
```

Run the Streamlit app with:

```bash
poetry run streamlit run app.py
```