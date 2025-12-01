from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import sys
import os
from pydantic import BaseModel

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from meetops.db import init_db
from meetops.agents.pipeline import process_meeting

load_dotenv()
init_db()

app = FastAPI(title="MeetOps - Meeting Automation Agent", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/process_meeting")
async def process_meeting_endpoint(file: UploadFile = File(...)):
    content_bytes = await file.read()
    text = content_bytes.decode("utf-8", errors="ignore")
    result = process_meeting(text)
    return result

class MeetingRequest(BaseModel):
    raw_text: str

@app.post("/process_meeting_json")
async def process_meeting_json(request: MeetingRequest):
    result = process_meeting(request.raw_text)
    return result
