from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Local RAG API", 
    description="A fully local, private API to chat with your documents."
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Local RAG API. The server is alive and running!"}

if __name__ == "__main__":
    print("Starting the FastAPI server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)