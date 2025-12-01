import os
import requests
from meetops.agents.logger import log_event

def send_action_to_discord(task: str, owner: str, due_date: str, priority: str) -> dict:
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("DISCORD_WEBHOOK_URL not set")
        log_event("DiscordError", f"Webhook not set for task: {task}", "DISCORD_WEBHOOK_URL not set")
        return {"ok": False, "error": "DISCORD_WEBHOOK_URL not set"}
    message = (
        f"**Action Item:**\n"
        f"**Task:** {task}\n"
        f"**Owner:** {owner}\n"
        f"**Due Date:** {due_date}\n"
        f"**Priority:** {priority}"
    )
    data = {"content": message}
    try:
        resp = requests.post(webhook_url, json=data)
        print(f"Discord response: {resp.status_code} {resp.text}")
        log_event("DiscordResponse", f"Task: {task}", f"Status: {resp.status_code}, Text: {resp.text}")
        if resp.status_code == 204:
            return {"ok": True}
        else:
            log_event("DiscordError", f"Task: {task}", f"HTTP {resp.status_code}: {resp.text}")
            return {"ok": False, "error": f"HTTP {resp.status_code}: {resp.text}"}
    except Exception as e:
        print(f"Discord exception: {e}")
        log_event("DiscordException", f"Task: {task}", str(e))
        return {"ok": False, "error": str(e)}
