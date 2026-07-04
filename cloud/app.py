import json
import os
import urllib.request
import urllib.parse
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import PlainTextResponse, JSONResponse
import google.generativeai as genai

app = FastAPI()

# Load env variables (for local debug or cloud platforms)
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
GITHUB_PAT = os.environ.get("GITHUB_PAT")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "kamleshvyasindia/company-os")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def post_slack_message(channel, text):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "channel": channel,
        "text": text
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            if not res_data.get("ok"):
                print(f"Slack API error: {res_data.get('error')}")
    except Exception as e:
        print(f"Failed to post message to Slack: {e}")

def fetch_github_file(filepath):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filepath}"
    headers = {
        "Authorization": f"token {GITHUB_PAT}",
        "Accept": "application/vnd.github.v3.raw",
        "User-Agent": "FastAPI-Slack-Bot"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode("utf-8")
    except Exception as e:
        print(f"Failed to fetch {filepath} from GitHub: {e}")
        return f"Error: Could not retrieve {filepath}."

def process_query_async(channel, user_text):
    # Fetch key brain context files
    company_context = fetch_github_file("brain/company.md")
    projects_context = fetch_github_file("brain/projects.md")
    tasks_context = fetch_github_file("brain/tasks.md")
    scoreboard_context = fetch_github_file("scoreboard.md")
    
    context = f"""
You are the Deloitte India Education Practice Assistant. Use the following context about the company, active projects, tasks, and metrics to answer the user's question accurately.

---
SYSTEM CONTEXT:
---
[COMPANY PROFILE]
{company_context}

[ACTIVE PROJECTS DIRECTORY]
{projects_context}

[CENTRAL TASKS & PIPELINE]
{tasks_context}

[SCOREBOARD & METRICS]
{scoreboard_context}
---

Provide a clear, professional, and concise response. Format the response with Slack markdown (*bold*, _italics_, bullet points). Cite filenames if relevant.
"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([context, f"User Question: {user_text}"])
        answer = response.text.strip()
    except Exception as e:
        print(f"Gemini API inference error: {e}")
        answer = "⚠️ Sorry, I encountered an error while processing your request. Please check if my Gemini API key is configured correctly."
        
    post_slack_message(channel, answer)

@app.post("/api/slack")
async def slack_webhook(request: Request, background_tasks: BackgroundTasks):
    body = await request.body()
    try:
        data = json.loads(body.decode("utf-8"))
    except json.JSONDecodeError:
        return PlainTextResponse("Invalid JSON", status_code=400)
        
    # Handle Slack Webhook challenge handshake verification
    if data.get("type") == "url_verification":
        return PlainTextResponse(data.get("challenge"))
        
    # Handle Slack event callback
    if data.get("type") == "event_callback":
        event = data.get("event", {})
        event_type = event.get("type")
        
        # Process message or mention, ignoring bot messages to avoid loops
        if event_type in ["message", "app_mention"] and not event.get("bot_id"):
            channel = event.get("channel")
            text = event.get("text", "")
            
            # Delegate heavy retrieval and AI response to background tasks to respond to Slack in <3 seconds
            background_tasks.add_task(process_query_async, channel, text)
            
    return JSONResponse(content={"ok": True})

@app.get("/")
def home():
    return {"status": "running", "bot": "Deloitte Education Brain"}
