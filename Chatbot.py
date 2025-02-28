import streamlit as st
from openai import OpenAI
from os import environ
import pypdf
from langchain.text_splitter import RecursiveCharacterTextSplitter

st.title("🤖 Awesome Chatbot")
st.caption("Powered by Yuning Wang")

# Function to extract text from PDFs
def extract_text_from_pdf(uploaded_file):
    """Extract text from an uploaded PDF file."""
    pdf_reader = pypdf.PdfReader(uploaded_file)
    return "\n".join([page.extract_text() or "" for page in pdf_reader.pages])

# Function to extract text from text files
def extract_text_from_txt(uploaded_file):
    """Extract text from a .txt file."""
    return uploaded_file.read().decode("utf-8")

# Function to split text into manageable chunks
def chunk_text(text, chunk_size=512, overlap=50):
    """Breaks text into smaller chunks for efficient retrieval."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return text_splitter.split_text(text)

# File uploader (supports multiple files)
uploaded_files = st.file_uploader("Upload documents (.txt, .pdf) (Optional)", type=["txt", "pdf"], accept_multiple_files=True)

# Dictionary to store processed documents
documents = {}

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_type = uploaded_file.type
        file_name = uploaded_file.name

        if file_type == "text/plain":
            file_content = extract_text_from_txt(uploaded_file)
        elif file_type == "application/pdf":
            file_content = extract_text_from_pdf(uploaded_file)
        else:
            file_content = ""

        if file_content:
            documents[file_name] = chunk_text(file_content)

# Sidebar display for uploaded files
if documents:
    st.sidebar.subheader("Uploaded Files")
    st.sidebar.write(list(documents.keys()))
else:
    st.sidebar.info("No files uploaded. Chatbot works normally!")

# Combine all document chunks into a single context
combined_context = ""
if documents:
    combined_context = "\n\n".join(["\n".join(chunks) for chunks in documents.values()])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

# Display previous chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input (always enabled)
question = st.chat_input("Ask something!")

if question:
    client = OpenAI(api_key=environ.get("OPENAI_API_KEY"))

    # Append user's message
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    with st.chat_message("assistant"):
        response_container = st.empty()
        response_text = ""

        # OpenAI API call with or without document context
        system_message = (
            f"Here's the content of all uploaded files:\n\n{combined_context}"
            if combined_context else
            "You are a helpful AI assistant. Answer questions conversationally."
        )

        stream = client.chat.completions.create(
            model="openai.gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                *st.session_state.messages
            ],
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                response_text += chunk.choices[0].delta.content
                response_container.write(response_text)

    # Append assistant's response
    st.session_state.messages.append({"role": "assistant", "content": response_text})



