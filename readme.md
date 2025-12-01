# MeetOps Agent

MeetOps Agent is an AI-powered automation platform for streamlining meeting operations, feedback management, production planning, and team communications. It leverages advanced AI/ML models to extract actionable insights from operational data and integrates with Discord and calendar systems for workflow automation.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Setup](#setup)
- [Usage](#usage)
- [Database](#database)
- [Agents](#agents)
- [Tools Integration](#tools-integration)
- [Logging](#logging)
- [Contributing](#contributing)
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
├── agents/          # Core agent logic (logger, pipeline)
├── db/              # Database models and access
├── tools/           # Integrations (calendar, Discord)
├── logs/            # Log files
├── app.py           # Main application entry point
├── main.py          # Alternate entry point or CLI
├── requirements.txt # Python dependencies
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
   - Update database connection settings in `meetops/db/models.py` if needed.

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

## Database
- SQLite database file: `meetops.db`
- Models defined in `meetops/db/models.py`
- Stores feedback, reviews, planning data, and operational metrics.

## Agents
- **Logger Agent:** Handles logging and monitoring.
- **Pipeline Agent:** Orchestrates transcript cleaning, action extraction, and task assignment.

## Tools Integration
- **Calendar Tool:** Automates scheduling and reminders.
- **Discord Tool:** Integrates with Discord for team communications and notifications.

## Logging
- All operational logs are stored in `logs/agent_logs.txt` for monitoring and debugging.

## Contributing
1. Fork the repository and create your feature branch (`git checkout -b feature/YourFeature`)
2. Commit your changes (`git commit -am 'Add new feature'`)
3. Push to the branch (`git push origin feature/YourFeature`)
4. Open a pull request

## License
This project is licensed under the MIT License.
