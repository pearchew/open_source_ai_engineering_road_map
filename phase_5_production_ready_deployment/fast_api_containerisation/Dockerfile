# 1. Use an official, lightweight Python runtime as a base image
FROM python:3.10-slim

# 2. Set the working directory inside the container to /app
WORKDIR /app

# 3. Copy ONLY the requirements file first (this helps Docker cache dependencies and build faster next time)
COPY requirements.txt .

# 4. Install the Python dependencies safely
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code (app.py) into the container
COPY . .

# 6. Expose port 8000 so the outside world can talk to FastAPI
EXPOSE 8000

# 7. Define the command to start the server when the container runs
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]