from typing import Dict

def create_event(title: str, description: str, date: str) -> Dict:
    print(f"[CalendarTool] Creating event: '{title}' on {date}. Description: {description}")
    return {
        "status": "ok",
        "title": title,
        "date": date,
        "description": description,
    }
