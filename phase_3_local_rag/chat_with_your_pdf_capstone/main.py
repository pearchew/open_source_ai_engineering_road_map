# go to http://localhost:8000/docs to see the interactive API documentation 
# fastAPI acts like a universal translator, automatically generating the perfect custom UI for every single "door" 
# (endpoint) you build, based entirely on the Python hints you write.

# 1. It Color-Codes the "Action" (HTTP Methods)
    # In web development, different doors are meant for different actions, and Swagger UI color-codes them so you can read your API like a map:
    # GET (Blue Box): For retrieving data. (Like our app.get("/") door that just returns the welcome message). It doesn't give you an upload button; it just gives you an "Execute" button to fetch the info.
    # POST (Green Box): For sending new data to the server. (Like our /ingest door).
    # PUT (Orange Box): For updating or editing existing data.
    # DELETE (Red Box): For deleting data.
# 2. It Adapts to the Input Type

import os
import shutil
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import uvicorn
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from sentence_transformers import CrossEncoder

print("Initializing Embeddings (Ensure Ollama is running!)...")
embeddings = OllamaEmbeddings(model="nomic-embed-text")
persist_directory = "./chroma_db"
llm = Ollama(model="llama3.1")
reranker = CrossEncoder("BAAI/bge-reranker-base")

app = FastAPI(
    title="Local RAG API", 
    description="A fully local, private API to chat with your documents."
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Local RAG API. The server is alive and running!"}

@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")
    
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        loader = PyPDFLoader(temp_file_path)
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(docs)
        
        vector_db = Chroma.from_documents(
            documents=chunks, 
            embedding=embeddings, 
            persist_directory=persist_directory
        )
        
        os.remove(temp_file_path)
        
        return {
            "message": f"Successfully processed {file.filename}!",
            "chunks_saved": len(chunks)
        }
        
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        return {"error": str(e)}

class AskRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask_question(request: AskRequest):
    query = request.query
    print(f"\nUser asked: '{query}'")
    
    vector_db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    
    broad_results = vector_db.similarity_search(query, k=10)
    if not broad_results:
        return {"answer": "My database is empty! Please upload a PDF to /ingest first."}
        
    pairs = [[query, doc.page_content] for doc in broad_results]
    scores = reranker.predict(pairs)
    scored_docs = zip(broad_results, scores)
    sorted_docs = sorted(scored_docs, key=lambda x: x[1], reverse=True)
    
    top_chunks = [doc.page_content for doc, score in sorted_docs[:3]]
    
    context_text = "\n\n---\n\n".join(top_chunks)
    
    prompt = f"""You are a helpful, brilliant assistant. Use ONLY the provided context to answer the user's question. 
    If the answer is not in the context, do not guess. Just say "I cannot answer this based on the provided documents."
    
    Context from Database:
    {context_text}

    User Question:
    {query}

    Your Answer:"""
    
    # 5. Generate the answer!
    print("Thinking...")
    answer = llm.invoke(prompt)
    print("Done!")
    
    # 6. Return the answer AND the sources we used to get it
    return {
        "question": query,
        "answer": answer,
        "sources_used": top_chunks
    }

if __name__ == "__main__":
    print("Starting the FastAPI server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)