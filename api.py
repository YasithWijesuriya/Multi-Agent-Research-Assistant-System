# api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from main import run_research

app = FastAPI(title="ResearchHub API")

# React frontend එකෙන් call කරන්න CORS enable කරනවා
origins = [
    "http://localhost:3000"  # React dev server default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint for research
@app.post("/research")
async def research_topic(payload: dict):
    topic = payload.get("topic", "")
    if not topic:
        return {"error": "Topic is required"}
    
    report = run_research(topic)
    return {"report": report}
# To run the API, use: uvicorn api:app --reload