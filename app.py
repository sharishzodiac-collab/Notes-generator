import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai

load_dotenv()

app = FastAPI()

# Allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Data received from frontend
class TranscriptRequest(BaseModel):
    transcript: str


@app.post("/generate-notes")
def generate_notes(request: TranscriptRequest):

    prompt = f"""
You are an AI meeting note-taking assistant.

Convert the following meeting transcript into clear and organized notes.

Use these sections:

1. Summary
2. Key Points
3. Decisions
4. Action Items
5. Deadlines

Do not change the meaning of the transcript.

Transcript:

{request.transcript}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return {
        "notes": response.text
    }


# Backend health check
@app.get("/api/health")
def health():
    return {
        "message": "Meeting Notes AI backend is running"
    }


# Serve frontend
app.mount(
    "/",
    StaticFiles(directory="frontend1", html=True),
    name="frontend"
)