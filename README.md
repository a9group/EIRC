# Enterprise IRC MVP

## Overview
This MVP implements an Enterprise IRC solution integrated with Jira and GitHub notifications. Notifications can optionally forward to Slack.

## Components
- **IRC Server:** InspIRCd
- **Web Client:** The Lounge
- **Notification Gateway:** Python FastAPI

## Setup Instructions

### 1. Configure
- Edit `notification-gateway/config.ini` to match your environment:
  - IRC details (server, port, channel)
  - Slack webhook (optional)

### 2. Launch
```bash
docker-compose up -d --build
```

### 3. Configure Webhooks
- **Jira Webhook URL:** `http://<your-host>:8000/webhooks/jira`
- **GitHub Webhook URL:** `http://<your-host>:8000/webhooks/github`