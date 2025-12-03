import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
import streamlit as st
import requests
import json
from fastapi import FastAPI, Request
from pydantic import BaseModel
from meetops.agents.pipeline import process_meeting

API_URL = "https://meetopsagent.onrender.com/process_meeting"
# API_URL = "http://127.0.0.1:8000/process_meeting"

app = FastAPI()

class MeetingRequest(BaseModel):
    raw_text: str

@app.post("/process_meeting")
def process_meeting_api(request: MeetingRequest):
    result = process_meeting(request.raw_text)
    return result

st.title("MeetOps – Automate Your Meeting Operations")
st.write("Easily automate your meeting workflow: upload a transcript (.txt) and let MeetOps clean the text, extract actionable tasks, assign owners and due dates, and create calendar events, all in one step!")

uploaded_file = st.file_uploader("Upload transcript", type=["txt"])

if uploaded_file is not None:
    transcript_text = uploaded_file.read().decode("utf-8")
    if st.button("Process Meeting"):
        payload = {"raw_text": transcript_text}
        with st.spinner("Processing..."):
            resp = requests.post(API_URL, json=payload)

        if resp.status_code != 200:
            st.error(f"Error from API: {resp.status_code} - {resp.text}")
        else:
            data = resp.json()
            st.subheader("Cleaned Transcript")
            st.text(data.get("cleaned_transcript", ""))

            st.subheader("Extracted Actions (JSON)")
            st.code(data.get("actions_json", ""), language="json")

            st.subheader("Execution Results")
            st.json(data.get("execution_results", {}))

            st.success(f"Stored meeting_id: {data.get('meeting_id')}")

            if "error" in data and data["error"]:
                st.error(data["error"])
                st.stop()
