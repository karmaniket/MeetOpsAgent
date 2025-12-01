import os
import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "agent_logs.txt")

def log_event(agent_name: str, input_snippet: str, output_snippet: str):
    timestamp = datetime.datetime.utcnow().isoformat()
    input_short = (input_snippet or "")[:300]
    output_short = (output_snippet or "")[:300]

    line = f"[{timestamp}] {agent_name} | INPUT: {input_short} | OUTPUT: {output_short}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)
