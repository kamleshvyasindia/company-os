import json
import os
import urllib.request
import urllib.parse
import urllib.error
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import PlainTextResponse, JSONResponse

app = FastAPI()

# Load env variables
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
GITHUB_PAT = os.environ.get("GITHUB_PAT")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "kamleshvyasindia/company-os")

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

def get_available_models():
    # Call ListModels to see what models this key can access
    url = f"https://generativelanguage.googleapis.com/v1/models?key={GEMINI_API_KEY}"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            models = res_data.get("models", [])
            model_names = [m.get("name") for m in models]
            return f"Authorized Models: {', '.join(model_names)}"
    except urllib.error.HTTPError as he:
        error_body = he.read().decode("utf-8")
        return f"ListModels failed: {he.code} - {error_body}"
    except Exception as e:
        return f"ListModels error: {e}"

def call_gemini_rest(context, query):
    prompt = f"{context}\n\nUser Question: {query}"
    
    api_versions = ["v1", "v1beta"]
    models = ["gemini-1.5-flash", "gemini-pro"]
    
    for ver in api_versions:
        for model in models:
            url = f"https://generativelanguage.googleapis.com/{ver}/models/{model}:generateContent?key={GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            }
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            try:
                print(f"Attempting REST API {ver} with model {model}...")
                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    candidates = res_data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            text_res = parts[0].get("text", "").strip()
                            print(f"Success using REST API {ver} with model {model}!")
                            return text_res
            except urllib.error.HTTPError as he:
                error_body = he.read().decode("utf-8")
                print(f"REST API {ver}/{model} failed with HTTPError: {he.code} - {error_body}")
            except Exception as e:
                print(f"REST API {ver}/{model} failed: {e}")
                
    return None

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
    
    answer = call_gemini_rest(context, user_text)
    
    if not answer:
        # If it fails, report the ListModels diagnostics directly to Slack to see why
        diagnostics = get_available_models()
        answer = f"⚠️ Gemini inference failed.\n\n*Diagnostics Output:*\n`{diagnostics}`"
        
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
