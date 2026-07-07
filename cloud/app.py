import json
import os
import urllib.request
import urllib.parse
import urllib.error
import io
import csv
import sys
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import PlainTextResponse, JSONResponse

app = FastAPI()

# Configure path imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import parse_data
import build_dashboard

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

def push_to_github(filepath, content, commit_message):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filepath}"
    headers = {
        "Authorization": f"token {GITHUB_PAT}",
        "Accept": "application/json",
        "User-Agent": "FastAPI-Slack-Bot"
    }
    sha = None
    try:
        get_req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(get_req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            sha = res_data.get("sha")
    except Exception as e:
        print(f"Could not get SHA for {filepath}: {e}")
        
    import base64
    b64_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    
    payload = {
        "message": commit_message,
        "content": b64_content
    }
    if sha:
        payload["sha"] = sha
        
    data = json.dumps(payload).encode("utf-8")
    put_req = urllib.request.Request(url, data=data, headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(put_req) as response:
            print(f"Successfully pushed {filepath} to GitHub!")
            return True
    except Exception as e:
        print(f"Failed to PUT {filepath} to GitHub: {e}")
        return False

def get_available_models():
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

def call_gemini_rest(prompt):
    api_versions = ["v1", "v1beta"]
    models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-3.5-flash", "gemini-1.5-flash"]
    
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
                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    candidates = res_data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            return parts[0].get("text", "").strip()
            except Exception as e:
                pass
    return None

def parse_task_nlp(user_text):
    prompt = f"""
Parse the following user request to add a new task. Extract:
1. action: The action or check required.
2. who: The owner of the task (e.g. KV, Mansi, Rajat, Deependra, Arvind, Priyank, Bhavisha, Meethi, Harshit). Convert to uppercase initials (e.g. KV) or capitalized name.
3. when: The due date (e.g. July 15, 2026 or August 10, 2026). Standardize to "Month DD, YYYY" format if possible, otherwise use "ASAP".
4. remarks: Any additional details (for example, "for May and June" or "follow up").

Input Text: "{user_text}"

Return ONLY a raw JSON object with keys "action", "who", "when", "remarks". Do not include any markdown styling, code blocks, or extra text.
"""
    res = call_gemini_rest(prompt)
    if res:
        try:
            if res.startswith("```"):
                res = res.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
            return json.loads(res)
        except Exception as e:
            print(f"JSON load failed on: {res}. Error: {e}")
    return None

def parse_win_nlp(user_text):
    prompt = f"""
Parse the following user request to add a new win or near win. Extract:
1. name: Opportunity Name (e.g. GSBTM PMU, Gujarat)
2. stage: Sales Stage (e.g. Won, Closed, WO received)
3. amount: Total Amount in INR Lakhs (e.g. 84 or 40. Do not write Lakhs, just the number).
4. pm: Project Manager or Owner (e.g. Priyank Patel, Debtirtha Bannerjee)
5. amount_pm: Monthly value in INR Lakhs (Total amount divided by duration in months, or write "-").
6. start: Start Date (e.g. August 1, 2026)
7. duration: Duration (e.g. 12 months)
8. hires: Additional Hires (e.g. 2 or 4)
9. remarks: Additional remarks
10. status: Hiring status (e.g. Avinash as EM)

Input Text: "{user_text}"

Return ONLY a raw JSON object with the keys "name", "stage", "amount", "pm", "amount_pm", "start", "duration", "hires", "remarks", "status". Do not include any markdown styling, code blocks, or extra text.
"""
    res = call_gemini_rest(prompt)
    if res:
        try:
            if res.startswith("```"):
                res = res.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
            return json.loads(res)
        except Exception as e:
            print(f"JSON load failed on: {res}. Error: {e}")
    return None

def execute_add_task(channel, user_text):
    parsed = parse_task_nlp(user_text)
    if not parsed:
        post_slack_message(channel, "❌ Failed to parse task details. Please verify your message format (e.g. `add task: Check WO status due July 15 owner KV`).")
        return
        
    csv_filename = "Pending Actions  July 2026.csv"
    csv_content = fetch_github_file(csv_filename)
    if "Error" in csv_content:
        post_slack_message(channel, f"❌ Failed to fetch current task list from GitHub: {csv_content}")
        return
        
    # Parse CSV content
    rows = []
    f = io.StringIO(csv_content)
    reader = csv.reader(f)
    for r in reader:
        rows.append(r)
        
    # Append new task row
    next_sno = str(len(rows))
    new_row = [next_sno, parsed.get("action"), parsed.get("who"), parsed.get("when", "ASAP"), parsed.get("remarks", "")]
    rows.append(new_row)
    
    # Save CSV back
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerows(rows)
    new_csv_content = out.getvalue()
    
    # Write to local file for generators to load
    local_csv_path = os.path.join(parse_data.base_path, csv_filename)
    with open(local_csv_path, "w", encoding="utf-8") as lf:
        lf.write(new_csv_content)
        
    # Regenerate task directory and dashboard locally
    try:
        parse_data.generate_tasks_md()
        build_dashboard.build()
    except Exception as e:
        print(f"In-process compilation failed: {e}")
        
    # Read compiled directories and dashboard
    tasks_md_path = os.path.join(parse_data.base_path, "brain", "tasks.md")
    dashboard_html_path = os.path.join(parse_data.base_path, "dashboard.html")
    
    with open(tasks_md_path, "r", encoding="utf-8") as f:
        updated_tasks_md = f.read()
    with open(dashboard_html_path, "r", encoding="utf-8") as f:
        updated_dashboard_html = f.read()
        
    # Push all updated files to GitHub
    push_to_github(csv_filename, new_csv_content, f"Add task: {parsed.get('action')} via Slack")
    push_to_github("brain/tasks.md", updated_tasks_md, "Regenerate tasks.md via Slack")
    push_to_github("dashboard.html", updated_dashboard_html, "Regenerate dashboard.html via Slack")
    
    success_msg = f"✅ *Task Added Successfully!*\n• *S.No:* {next_sno}\n• *Action:* {parsed.get('action')}\n• *Who:* {parsed.get('who')}\n• *When:* {parsed.get('when')}\n• *Remarks:* {parsed.get('remarks') or '—'}\n\n_GitHub repository and Web Dashboard have been updated!_"
    post_slack_message(channel, success_msg)

def execute_add_win(channel, user_text):
    parsed = parse_win_nlp(user_text)
    if not parsed:
        post_slack_message(channel, "❌ Failed to parse project win details. Please verify your message format (e.g. `add win: GSBTM PMU value 84L owner Priyank EM Avinash`).")
        return
        
    csv_filename = "Wins and Near wins July 2026.csv"
    csv_content = fetch_github_file(csv_filename)
    if "Error" in csv_content:
        post_slack_message(channel, f"❌ Failed to fetch current wins pipeline from GitHub: {csv_content}")
        return
        
    # Parse CSV content
    rows = []
    f = io.StringIO(csv_content)
    reader = csv.reader(f)
    for r in reader:
        rows.append(r)
        
    # Find insertion point (just before the total row)
    insert_idx = -1
    for i, r in enumerate(rows):
        if len(r) > 1 and "total in inr" in r[1].lower():
            insert_idx = i
            break
    if insert_idx == -1:
        insert_idx = len(rows)
        
    # Construct new row
    sno = str(insert_idx - 1)
    new_row = [
        sno,
        parsed.get("name"),
        parsed.get("stage", "Won"),
        parsed.get("amount"),
        parsed.get("jup_id", ""),
        parsed.get("pm"),
        parsed.get("amount_pm", "-"),
        parsed.get("start", "ASAP"),
        parsed.get("duration", "12 months"),
        parsed.get("hires", "0"),
        parsed.get("remarks", ""),
        parsed.get("status", "")
    ]
    rows.insert(insert_idx, new_row)
    
    # Recalculate Total (Column index 3 is amount)
    total_val = 0
    for r in rows[2:insert_idx+1]:
        val_str = r[3].replace(",", "").strip()
        if val_str:
            try:
                total_val += float(val_str)
            except ValueError:
                pass
                
    # Update Total row (which is now at insert_idx + 1)
    rows[insert_idx + 1][3] = f"{total_val:.1f}"
    
    # Save CSV back
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerows(rows)
    new_csv_content = out.getvalue()
    
    # Write to local file for generators
    local_csv_path = os.path.join(parse_data.base_path, csv_filename)
    with open(local_csv_path, "w", encoding="utf-8") as lf:
        lf.write(new_csv_content)
        
    # Regenerate dashboard locally
    try:
        build_dashboard.build()
    except Exception as e:
        print(f"Dashboard compilation failed: {e}")
        
    # Read compiled dashboard
    dashboard_html_path = os.path.join(parse_data.base_path, "dashboard.html")
    with open(dashboard_html_path, "r", encoding="utf-8") as f:
        updated_dashboard_html = f.read()
        
    # Push updated files to GitHub
    push_to_github(csv_filename, new_csv_content, f"Add win: {parsed.get('name')} via Slack")
    push_to_github("dashboard.html", updated_dashboard_html, "Regenerate dashboard.html via Slack")
    
    # Also update scoreboard metrics
    scoreboard_path = os.path.join(parse_data.base_path, "scoreboard.md")
    if os.path.exists(scoreboard_path):
        with open(scoreboard_path, "r", encoding="utf-8") as sf:
            sb_content = sf.read()
        # Find Pipeline Row and update total win value
        lines = sb_content.split("\n")
        for idx, line in enumerate(lines):
            if "BD Proposal Volume" in line:
                # Update NSR pipeline value
                lines[idx] = f"| BD Proposal Volume / Pipeline | TBD | ₹{total_val/100:.3f} Cr (Wins & Near Wins) | | Added {parsed.get('name')} via Slack |"
                break
        new_sb_content = "\n".join(lines)
        with open(scoreboard_path, "w", encoding="utf-8") as sf:
            sf.write(new_sb_content)
        push_to_github("scoreboard.md", new_sb_content, "Update scoreboard metrics via Slack")
        
    success_msg = f"🏆 *New Project Win Added Successfully!*\n• *Opportunity:* {parsed.get('name')}\n• *Total Value:* ₹{parsed.get('amount')} L\n• *PM:* {parsed.get('pm')}\n• *Start Date:* {parsed.get('start')}\n• *New Pipeline Total:* ₹{total_val/100:.3f} Crore\n\n_GitHub repository, Scoreboard, and Web Dashboard have been updated!_"
    post_slack_message(channel, success_msg)

def execute_query(channel, user_text):
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
    
    answer = call_gemini_rest(f"{context}\n\nUser Question: {user_text}")
    
    if not answer:
        diagnostics = get_available_models()
        answer = f"⚠️ Gemini inference failed.\n\n*Diagnostics Output:*\n`{diagnostics}`"
        
    post_slack_message(channel, answer)

def process_query_async(channel, user_text):
    user_clean = user_text.strip().lower()
    
    # Routing: check if command is to add a task
    if user_clean.startswith("add task:") or user_clean.startswith("task:"):
        execute_add_task(channel, user_text)
    # Routing: check if command is to add a win
    elif user_clean.startswith("add win:") or user_clean.startswith("win:"):
        execute_add_win(channel, user_text)
    # Default routing: process as Q&A
    else:
        execute_query(channel, user_text)

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
