import os
from dotenv import load_dotenv
import json
from typing import Dict, Any, List
from meetops.db import SessionLocal, Meeting
from meetops.agents.logger import log_event
from meetops.tools import create_event
from meetops.tools.discord_tool import send_action_to_discord
import time
import google.generativeai as genai

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set. Configure it in .env or environment variables.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def ask_llm(system_prompt: str, user_prompt: str) -> str:
    prompt = system_prompt + "\n" + user_prompt
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        log_event("GeminiError", prompt, str(e))
        return None

def get_project_context(db) -> str:
    recent_meetings: List[Meeting] = (
        db.query(Meeting)
        .order_by(Meeting.created_at.desc())
        .limit(3)
        .all()
    )
    if not recent_meetings:
        return ""
    chunks = []
    for m in recent_meetings:
        chunks.append(f"- Previous meeting summary:\n{m.cleaned_transcript[:500]}")

    return "\n\n".join(chunks)

def ingestion_agent(raw_text: str, context: str) -> str:
    system_prompt = (
        "You are a meeting ingestion agent. "
        "You clean transcripts, remove filler words, fix obvious typos, "
        "and keep speaker names and structure. "
        "You do NOT invent content."
    )
    user_prompt = (
        f"Here is some project context from previous meetings (may be empty):\n"
        f"{context}\n\n"
        f"Now clean the following new meeting transcript. "
        f"Return only the cleaned transcript text.\n\n"
        f"--- RAW TRANSCRIPT ---\n{raw_text}"
    )
    cleaned = ask_llm(system_prompt, user_prompt)
    if cleaned is None:
        return "FAILED: LLM could not process this transcript. Possibly too large or invalid."
    log_event("IngestionAgent", raw_text, cleaned)
    return cleaned

def action_agent(cleaned_text: str) -> str:
    import datetime
    system_date = datetime.datetime.now().strftime('%Y-%m-%d')
    system_prompt = (
        "You are an action extraction agent. "
        "Your job is to read a cleaned meeting transcript and extract ALL action items. "
        f"Use the system date ({system_date}) as reference for the entire due dates. "
        "Each action item must include: task, owner (if known), due_date (if known), priority (HIGH/MEDIUM/LOW). "
        "If owner or due_date is not clear, set them to null. "
        "For each line, if a task is mentioned, use the speaker as the owner unless the task is clearly assigned to someone else. "
        f"Extract due dates from phrases like 'by Thursday', 'by Wednesday evening', 'Friday 3 PM', etc., and use the system date ({system_date}) as reference. "
        "If a time is mentioned, include it in the due_date in a globally accessible format, e.g., 'YYYY-MM-DD 3:00 PM', not ISO THH:MM:SS. Use AM/PM notation for times. "
        "If the transcript mentions missed SLAs, tickets, or issues, create an action item to investigate or follow up, including ticket numbers or identifiers. "
        "For investigation or follow-up tasks (e.g., 'Root cause?'), assign the speaker as the owner unless another person is clearly responsible. "
        "If a high-priority investigation or incident follow-up task does not have a specified due date, set the due date to the next business day after the meeting (e.g., if the meeting is on the system date, use the next business day). "
    )

    user_prompt = (
        "Extract all action items from this meeting transcript. "
        "Return ONLY valid JSON in the following format:\n\n"
        "[\n"
        "  {\n"
        '    "task": "...",\n'
        '    "owner": "... or null",\n'
        '    "due_date": "YYYY-MM-DD or null",\n'
        '    "priority": "HIGH" | "MEDIUM" | "LOW"\n'
        "  },\n"
        "  ...\n"
        "]\n\n"
        "Transcript:\n"
        f"{cleaned_text}"
    )

    actions_json = ask_llm(system_prompt, user_prompt)
    if actions_json is None:
        return "[]"
    if not actions_json.strip():
        return "[]"
    try:
        json.loads(actions_json)
    except:
        actions_json = "[]"
    log_event("ActionAgent", cleaned_text, actions_json)
    return actions_json

def task_assignment_agent(actions: list, use_discord: bool = False) -> list:
    results = []
    for action in actions:
        task = action.get("task", "Untitled task")
        owner = action.get("owner") or "Unassigned"
        due_date = action.get("due_date", "unspecified date")
        priority = action.get("priority", "MEDIUM")
        result = send_action_to_discord(task, owner, due_date, priority)
        if not result.get("ok"):
            log_event("DiscordError", str(action), str(result.get("error")))
        results.append(result)
    return results

def execution_agent(actions_json: str) -> Any:
    start_time = time.time()
    try:
        actions = json.loads(actions_json)
        if not isinstance(actions, list):
            raise ValueError("actions_json is not a list")
    except Exception as e:
        log_event("ExecutionAgent", actions_json, f"JSON parse error: {e}")
        return {"error": f"Failed to parse actions JSON: {e}"}

    results = []
    for action in actions:
        task = action.get("task", "Untitled task")
        due_date = action.get("due_date", "unspecified date")
        owner = action.get("owner") or "Unassigned"
        priority = action.get("priority", "MEDIUM")

        description = f"Owner: {owner}, Priority: {priority}"
        result = create_event(title=task, description=description, date=due_date)
        results.append(result)

    use_discord = bool(os.getenv("DISCORD_WEBHOOK_URL"))
    send_results = task_assignment_agent(actions, use_discord=use_discord)
    metrics = {
        "num_actions": len(actions),
        "execution_time_sec": round(time.time() - start_time, 2)
    }
    log_event("ExecutionAgent", actions_json, json.dumps(results))
    log_event("Metrics", str(metrics), str(send_results))
    return {"calendar_results": results, "send_results": send_results, "metrics": metrics}

def process_meeting(raw_text: str) -> Dict[str, Any]:
    if len(raw_text) > 15000:
        return {
        "error": "Transcript too large. Please upload a smaller file (max ~15k characters)."
        }
    db = SessionLocal()

    try:
        context = get_project_context(db)
        cleaned = ingestion_agent(raw_text, context)
        if cleaned.startswith("FAILED"):
            return {
            "error": cleaned,
            "cleaned_transcript": "",
            "actions_json": "[]",
            "execution_results": {}
            }
        actions_json = action_agent(cleaned)
        execution_results = execution_agent(actions_json)

        meeting = Meeting(
            raw_transcript=raw_text,
            cleaned_transcript=cleaned,
            actions_json=actions_json,
        )
        db.add(meeting)
        db.commit()
        db.refresh(meeting)

        return {
            "meeting_id": meeting.id,
            "cleaned_transcript": cleaned,
            "actions_json": actions_json,
            "execution_results": execution_results,
        }
    finally:
        db.close()
