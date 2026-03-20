# Multi-AI Agent

A production-ready multi-agent AI system that routes natural language requests to specialized agents for task management, calendar scheduling, and reminders — powered by Google Gemini and LangGraph.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        React Frontend                        │
│                    (Vite · JWT Auth · Vercel)                │
└──────────────────────────┬──────────────────────────────────┘
                           │  HTTPS + Bearer Token
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     Django REST API                          │
│              (DRF · SimpleJWT · Railway)                     │
│                                                              │
│   POST /api/token/     →  Issue JWT                         │
│   POST /api/signup/    →  Register user                     │
│   POST /api/chat/      →  Process message                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    LangGraph Planner                         │
│           (Gemini LLM · JSON plan generation)                │
│                                                              │
│   "Schedule meeting and remind me to prepare slides"        │
│        ↓                                                     │
│   [{ agent: calendar_agent, task: "Schedule meeting" },     │
│    { agent: reminder_agent, task: "Prepare slides"  }]      │
└──────┬──────────────────┬──────────────────┬───────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌────────────┐   ┌─────────────────┐   ┌─────────────┐
│ Task Agent │   │ Calendar Agent  │   │Reminder Agent│
│            │   │                 │   │             │
│ create_task│   │  create_event   │   │create_remind│
│ list_tasks │   │                 │   │             │
└─────┬──────┘   └────────┬────────┘   └──────┬──────┘
      │                   │                   │
      └───────────────────┼───────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     PostgreSQL (Neon)                        │
│          Tasks · CalendarEvents · Reminders                  │
│              Conversations · Messages                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, plain CSS |
| Backend | Django 6, Django REST Framework |
| Auth | JWT via SimpleJWT |
| AI Orchestration | LangGraph state machine |
| LLM | Google Gemini via LangChain |
| Database | PostgreSQL (Neon) |
| Frontend Deploy | Vercel |
| Backend Deploy | Railway |

---

## Features

- Natural language routing to specialized agents
- JWT-based authentication with signup and login
- Execution plan displayed with each response (shows which agents ran)
- Persistent conversation and message history
- Task creation and listing
- Calendar event scheduling
- Reminder creation
- Clean dark-themed React UI

---

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- A Google Gemini API key ([get one here](https://aistudio.google.com/app/apikey))

### 1. Clone the repo

```bash
git clone https://github.com/your-username/multi-ai.git
cd multi-ai
```

### 2. Backend setup

```bash
cd multi_ai_agent
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file inside `multi_ai_agent/`:

```env
SECRET_KEY=any-long-random-string-for-local-dev
DEBUG=True
GOOGLE_API_KEY=your-gemini-api-key-here
DATABASE_URL="postgres Url"

```

For local development, switch to SQLite in `settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

Run migrations and create your user:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend runs at `http://localhost:8000`

### 3. Frontend setup

```bash
cd ai-agent-ui
npm install
cp .env.example .env
```

`.env` should contain:

```env
VITE_API_URL=http://localhost:8000
```

```bash
npm run dev
```

Frontend runs at `http://localhost:5173`

### 4. Log in

Use the superuser credentials you created, or sign up via the UI.

---

## Project Structure

```
multi-ai/
├── multi_ai_agent/          # Django backend
│   ├── ai_agents/
│   │   ├── agents.py        # LangChain agent definitions
│   │   ├── executor.py      # Plan execution engine
│   │   ├── graph.py         # LangGraph state machine
│   │   ├── llm.py           # Gemini model config
│   │   ├── planner.py       # AI plan generator
│   │   ├── tool_registry.py # Tool lookup map
│   │   ├── tools.py         # LangChain tools (task, event, reminder)
│   │   ├── urls.py          # API routes
│   │   └── views.py         # REST endpoints
│   ├── productivity/
│   │   └── models.py        # Task, CalendarEvent, Reminder, Conversation
│   ├── multi_ai_agent/
│   │   ├── settings.py
│   │   └── urls.py          # Root URL config
│   ├── Procfile             # Railway deployment
│   ├── requirements.txt
│   └── manage.py
│
└── ai-agent-ui/             # React + Vite frontend
    ├── src/
    │   ├── api/
    │   │   └── client.js    # API calls with JWT
    │   ├── components/
    │   │   ├── MessageBubble.jsx
    │   │   └── Sidebar.jsx
    │   ├── pages/
    │   │   ├── LoginPage.jsx
    │   │   └── ChatPage.jsx
    │   ├── styles/
    │   ├── App.jsx
    │   └── main.jsx
    ├── .env.example
    ├── index.html
    ├── package.json
    └── vite.config.js
```

---

## API Reference

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/token/` | None | Get JWT access token |
| POST | `/api/token/refresh/` | None | Refresh access token |
| POST | `/api/signup/` | None | Register new user |
| POST | `/api/chat/` | Bearer token | Send message to agents |

### POST `/api/chat/`

**Request:**
```json
{
  "message": "Schedule a meeting tomorrow and remind me to prepare slides"
}
```

**Response:**
```json
{
  "response": "Event 'Schedule a meeting tomorrow' scheduled. Reminder created: prepare slides",
  "plan": [
    { "agent": "calendar_agent", "task": "Schedule a meeting tomorrow" },
    { "agent": "reminder_agent", "task": "prepare slides" }
  ]
}
```

---

## Deployment

### Backend → Railway

1. Push code to GitHub
2. [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Set root directory to `multi_ai_agent`
4. Add environment variables:

```env
SECRET_KEY=<strong-random-string>
DEBUG=False
GOOGLE_API_KEY=<your-gemini-key>
DATABASE_URL="postgres Url"
```

5. After deploy, open Railway shell and run:
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Frontend → Vercel

1. [vercel.com](https://vercel.com) → New Project → Import repo
2. Set **Root Directory** to `ai-agent-ui`
3. Add environment variable:
```env
VITE_API_URL=https://your-backend.up.railway.app
```
4. Deploy

### Final step — update CORS

In `settings.py`:
```python
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.vercel\.app$",
]
```
Commit and push to trigger Railway redeploy.

---

## Environment Variables

### Backend (`.env`)

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for local, `False` for production |
| `GOOGLE_API_KEY` | Gemini API key |
| `DB_URL` | PostgreSQL database Url |

### Frontend (`.env`)

| Variable | Description |
|---|---|
| `VITE_API_URL` | Django backend base URL |

---

## License

MIT
