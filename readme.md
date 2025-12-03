# MeetOps Agent

MeetOps Agent is an AI-powered automation platform for streamlining meeting operations, feedback management, production planning, and team communications. It leverages advanced AI/ML models to extract actionable insights from operational data and integrates with Discord and calendar systems for workflow automation.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Setup](#setup)
- [Usage](#usage)
- [Deployment Configuration](#deployment-configuration)
- [Database](#database)
- [Agents](#agents)
- [Tools Integration](#tools-integration)
- [Logging](#logging)
- [License](#license)

## Overview
MeetOps Agent is an AI agent that automates the ingestion and analysis of meeting transcripts, extracts action items, assigns tasks, and notifies team members via Discord and calendar events. It is designed for data-driven organizations seeking to optimize operational efficiency and feedback loops.

## Features
- Automated meeting transcript cleaning and action extraction using AI
- Feedback and review management
- Production and marketing planning support
- Discord and calendar integration for notifications and scheduling
- Centralized logging and monitoring
- Extensible agent and tool architecture

## Architecture

```bash
meetops/
├── agents/          # Core agent logic
│  ├── __init__.py
│  ├── logger.py
│  └── pipeline.py
├── db/              # Database models and access
│  ├── __init__.py
│  ├── models.py
│  └── meetops.db
├── logs/            # Log file
│  └── agent_logs.txt
├── tools/           # Integrations
│  ├── __init__.py
│  ├── calendar_tool.py
│  └── discord_tool.py
├── __init__.py
├── .env             # API keys
├── app.py           # Main application entry point
├── main.py          # Alternate entry point or CLI
└── requirements.txt # Python dependencies
```

## Setup
1. **Clone the repository**
   ```powershell
   git clone https://github.com/karmaniket/MeetOpsAgent.git
   cd "d:\Project\Data_AI_ML\MeetOps Agent"
   ```
2. **Install dependencies**
   ```powershell
   pip install -r meetops/requirements.txt
   ```
3. **Configure environment**
   - Set up required environment variables (API keys for Discord, calendar integrations).
   - Update database connection settings in `db/models.py` if needed.

## Usage
- **Run the Streamlit frontend:**
  ```powershell
  streamlit run meetops/app.py
  ```
- **Run the FastAPI backend:**
  ```powershell
  uvicorn meetops.main:app --reload
  ```
- **Logs:**
  - Application logs are stored in `meetops/logs/agent_logs.txt`.

## Deployment Configuration
### Service 1: MeetOpsAgent
```bash
version: "1"
services:
- type: web
  name: MeetOpsAgent
  runtime: python
  repo: https://github.com/karmaniket/MeetOpsAgent
  plan: free
  envVars:
  - key: GEMINI_API_KEY
    sync: false
  region: oregon
  buildCommand: pip install -r meetops/requirements.txt
  startCommand: uvicorn meetops.main:app --host 0.0.0.0 --port $PORT
  autoDeployTrigger: commit
```
### Service 2: MeetOpsApp

```bash
version: "1"
services:
- type: web
  name: MeetOpsApp
  runtime: python
  repo: https://github.com/karmaniket/MeetOpsAgent
  plan: free
  envVars:
  - key: GEMINI_API_KEY
    sync: false
  region: oregon
  buildCommand: pip install -r meetops/requirements.txt
  startCommand: streamlit run meetops/app.py --server.port $PORT
  autoDeployTrigger: commit
```

## Database
- SQLite database file: `meetops.db`
- Models defined in `db/models.py`
- Stores feedback, reviews, planning data, and operational metrics.

## Agents
- **Logger Agent:** Handles logging and monitoring.
- **Pipeline Agent:** Orchestrates transcript cleaning, action extraction, and task assignment.

## Tools Integration
- **Calendar Tool:** Automates scheduling and reminders.
- **Discord Tool:** Integrates with Discord for team communications and notifications.

## Logging
- All operational logs are stored in `logs/agent_logs.txt` for monitoring and debugging.

## License
This project is licensed under the [MIT License](LICENSE).

You are free to use, modify, and distribute this software, provided that you include the original copyright notice and this license in any copies or substantial portions of the software. This ensures that credit and attribution are always given to the original author.