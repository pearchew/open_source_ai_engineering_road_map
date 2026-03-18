from pydantic import BaseModel
from fastapi import FastAPI

# 1. Initialize the FastAPI app
app = FastAPI(title="TEST API")

# We define a class that inherits from Pydantic's BaseModel
class LLMQuery(BaseModel):
    prompt: str
    # If a user sends a payload that doesn't perfectly match this structure (e.g., they send "temperature": "hot" instead of a float), 
    # Pydantic will automatically reject the request and send a helpful error message back to the user before the bad data ever touches your LLM logic.
    temperature: float = 0.7  # The '= 0.7' makes this optional with a default value
    max_tokens: int

# 3. Create a POST endpoint
# any time you see the @ symbol placed directly above a function, that is a decorator. 
    # Think of a decorator as a label or an instruction tag you attach to the function immediately below it.
        # @: This tells Python, "Hey, I'm about to attach some special behavior to the function right below me."
        # app: This is your FastAPI server manager (the one we created with app = FastAPI()). We are calling on it to do some work.
        # .post: This specifies the HTTP Method. It tells your server, "Only listen for POST requests here." If someone tries to send a GET request to this URL, the server will automatically reject it.
        # ("/generate"): This is the Path or Route. It tells the server where to listen.
@app.post("/generate")
async def generate_text(query: LLMQuery):
    # Because of Pydantic, we know 'query.prompt' is guaranteed to be a string!
    print(f"Received prompt: {query.prompt}")
    
    # We are faking the LLM response for now
    fake_response = f"This is a fake AI response to: '{query.prompt}'"
    
    return {
        "status": "success",
        "original_prompt": query.prompt,
        "response": fake_response,
        "settings_used": {
            "temp": query.temperature,
            "tokens": query.max_tokens
        }
    }
