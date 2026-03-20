import streamlit as st
import requests

# This is the address of your FastAPI server
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Local RAG Chat", page_icon="📚")
st.title("📚 Local Private RAG Chatbot")

# --- SIDEBAR: FILE UPLOAD ---
with st.sidebar:
    st.header("1. Upload a Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    
    if st.button("Process Document") and uploaded_file is not None:
        with st.spinner("Chunking and Embedding..."):
            # We package the file and send it to our FastAPI /ingest door
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            response = requests.post(f"{API_URL}/ingest", files=files)
            
            if response.status_code == 200:
                st.success(response.json().get("message"))
            else:
                st.error("Something went wrong during ingestion.")

# --- MAIN PAGE: CHAT INTERFACE ---
st.header("2. Chat with your Data")

# Streamlit re-runs the whole script on every click. 
# We use "session_state" to remember the chat history so it doesn't disappear!
if "messages" not in st.session_state:
    st.session_state.messages = []

# Draw the past chat messages on the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# The chat input box at the bottom of the screen
if prompt := st.chat_input("Ask a question about your PDF..."):
    
    # 1. Show the user's question on the screen immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Show a loading spinner while we wait for Llama 3.1
    with st.chat_message("assistant"):
        with st.spinner("Searching documents and thinking..."):
            
            # Send the text to our FastAPI /ask door
            payload = {"query": prompt}
            response = requests.post(f"{API_URL}/ask", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer")
                sources = data.get("sources_used", [])
                
                # Show the AI's answer
                st.markdown(answer)
                
                # Optional: Show the sources it used in a cool drop-down box!
                with st.expander("View Sources"):
                    for i, source in enumerate(sources):
                        st.write(f"**Source {i+1}:** {source}")
                
                # Save the answer to chat history
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("Failed to connect to the backend API. Is FastAPI running?")