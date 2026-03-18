# build a realistic simulation of an LLM backend. 
    # Instead of instantly returning a fake string, we will use asyncio.sleep(3) to artificially hold the connection open for 3 seconds. 
    # Because you are using async, your server won't freeze during this time—it will remain ready to accept other requests!

import asyncio
import time
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Async LLM Simulator")

class LLMRequest(BaseModel):
    prompt: str
    model_name: str

class LLMResponse(BaseModel):
    generated_text: str
    processing_time: float

@app.post("/generate", response_model=LLMResponse)
async def simulate_llm_generation(request_data: LLMRequest):
    print(f"Received prompt for {request_data.model_name}...")
    start_time = time.time()
    await asyncio.sleep(3)
    end_time = time.time()
    total_time = round(end_time - start_time, 2)
    return LLMResponse(
        generated_text=f"Hello! I am a simulated response to: '{request_data.prompt}'",
        processing_time=total_time)