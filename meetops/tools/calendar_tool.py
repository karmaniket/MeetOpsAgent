from typing import Dict

def create_event(title: str, description: str, date: str) -> Dict:
    """
    Simulated calendar tool.
    In real life, this would call Google Calendar / Trello / Jira API.
    """
    print(f"[CalendarTool] Creating event: '{title}' on {date}. Description: {description}")
    return {
        "status": "ok",
        "title": title,
        "date": date,
        "description": description,
    }
