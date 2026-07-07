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
import firebase_admin
from firebase_admin import credentials, firestore

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

# Initialize Firebase Admin
db = None
try:
    firebase_key = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY")
    if firebase_key:
        cred_dict = json.loads(firebase_key)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase initialized in app.py using env variable.")
    else:
        # Check local folder
        key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "firebase-key.json")
        if os.path.exists(key_path):
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("Firebase initialized in app.py using local key file.")
except Exception as e:
    print(f"Failed to initialize Firebase Admin: {e}")

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
    quoted_path = urllib.parse.quote(filepath)
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{quoted_path}"
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
    quoted_path = urllib.parse.quote(filepath)
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{quoted_path}"
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
    
    # Sync new task to Firestore
    if db:
        try:
            actions_ref = db.collection("team_actions")
            action_docs = actions_ref.get()
            doc_id = f"action_{len(action_docs)}"
            owner_clean = parsed.get("who", "").strip().lower().replace(".md", "").replace("people/", "")
            actions_ref.document(doc_id).set({
                "sno": next_sno,
                "action": parsed.get("action"),
                "owner": owner_clean,
                "targetDate": parsed.get("when", "ASAP"),
                "status": parsed.get("remarks", ""),
                "updatedAt": firestore.SERVER_TIMESTAMP
            })
            print(f"Synced task to Firestore document {doc_id}")
        except Exception as e:
            print(f"Failed to sync task to Firestore: {e}")
            
    success_msg = f"✅ *Task Added Successfully!*\n• *S.No:* {next_sno}\n• *Action:* {parsed.get('action')}\n• *Who:* {parsed.get('who')}\n• *When:* {parsed.get('when')}\n• *Remarks:* {parsed.get('remarks') or '—'}\n\n_GitHub repository, Firestore DB, and Web Dashboard have been updated!_"
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
        
        # Sync scoreboard to Firestore
        if db:
            try:
                db.collection("metadata").document("scoreboard").set({
                    "content": new_sb_content,
                    "updatedAt": firestore.SERVER_TIMESTAMP
                })
                print("Synced scoreboard to Firestore.")
            except Exception as e:
                print(f"Failed to sync scoreboard to Firestore: {e}")
        
    success_msg = f"🏆 *New Project Win Added Successfully!*\n• *Opportunity:* {parsed.get('name')}\n• *Total Value:* ₹{parsed.get('amount')} L\n• *PM:* {parsed.get('pm')}\n• *Start Date:* {parsed.get('start')}\n• *New Pipeline Total:* ₹{total_val/100:.3f} Crore\n\n_GitHub repository, Scoreboard, Firestore DB, and Web Dashboard have been updated!_"
    post_slack_message(channel, success_msg)

def get_company_context():
    if db:
        try:
            doc = db.collection("metadata").document("company").get()
            if doc.exists:
                return doc.to_dict().get("content", "")
        except Exception as e:
            print(f"Firestore get_company_context error: {e}")
    return fetch_github_file("brain/company.md")

def get_scoreboard_context():
    if db:
        try:
            doc = db.collection("metadata").document("scoreboard").get()
            if doc.exists:
                return doc.to_dict().get("content", "")
        except Exception as e:
            print(f"Firestore get_scoreboard_context error: {e}")
    return fetch_github_file("scoreboard.md")

def get_projects_context():
    if db:
        try:
            docs = db.collection("projects").stream()
            gov_lines = [
                "| WBS Code | Project Name | Client | Project Director (PD) | Engagement Manager (EM) | Value (INR) | Monthly Max (INR) | Deployed / Vacant / Resigned | Status / Notes |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"
            ]
            priv_lines = [
                "| Project Name | Client | Project Manager | Value (INR) | Monthly Max (INR) | Deployed | Duration / Timeline | Status |",
                "| --- | --- | --- | --- | --- | --- | --- | --- |"
            ]
            
            for doc in docs:
                d = doc.to_dict()
                ptype = d.get("type", "government")
                if ptype == "government":
                    gov_lines.append(f"| `{d.get('wbs','')}` | {d.get('name','')} | {d.get('client','')} | [[people/{d.get('director','')}.md]] | [[people/{d.get('manager','')}.md]] | {d.get('value','')} | {d.get('monthlyMax','')} | {d.get('staffing','')} | {d.get('status','')} |")
                else:
                    mgr = d.get('manager','')
                    mgr_link = f"[[people/{mgr}.md]]" if mgr else ""
                    priv_lines.append(f"| {d.get('name','')} | {d.get('client','')} | {mgr_link} | {d.get('value','')} | {d.get('monthlyMax','')} | {d.get('deployed','')} | {d.get('duration','')} | {d.get('status','')} |")
            
            return "# Active Projects Directory\n\nThis directory lists all active education and skills engagements across government and private sector clients.\n\n---\n\n## Government PMU Projects\n\n" + "\n".join(gov_lines) + "\n\n---\n\n## Private Sector & AI Training Projects\n\n" + "\n".join(priv_lines)
        except Exception as e:
            print(f"Firestore get_projects_context error: {e}")
    return fetch_github_file("brain/projects.md")

def get_tasks_context():
    if db:
        try:
            tasks = db.collection("tasks").stream()
            actions = db.collection("team_actions").stream()
            pipeline = db.collection("pipeline").stream()
            
            tasks_lines = [
                "| Date | Event / Meeting | Status | Remarks |",
                "| --- | --- | --- | --- |"
            ]
            action_lines = [
                "| S.No. | Action Required | Owner | Timeline | Remarks / Status |",
                "| --- | --- | --- | --- | --- |"
            ]
            pipeline_lines = [
                "| Opportunity Name | Sales Stage | Target Owner | Estimated Value (Lakhs) | Jupiter ID | Notes |",
                "| --- | --- | --- | --- | --- | --- |"
            ]
            
            tasks_list = []
            for doc in tasks:
                d = doc.to_dict()
                tasks_list.append(d)
            for d in tasks_list:
                tasks_lines.append(f"| {d.get('date','')} | {d.get('event','')} | {d.get('status','')} | {d.get('remarks','')} |")
                
            actions_list = []
            for doc in actions:
                d = doc.to_dict()
                actions_list.append(d)
            try:
                actions_list.sort(key=lambda x: int(x.get("sno", "999")))
            except Exception:
                pass
            for d in actions_list:
                owner = d.get('owner','')
                owner_link = f"[[people/{owner}.md]]" if owner else ""
                action_lines.append(f"| {d.get('sno','')} | {d.get('action','')} | {owner_link} | {d.get('targetDate','')} | {d.get('status','')} |")
                
            pipeline_list = []
            for doc in pipeline:
                d = doc.to_dict()
                pipeline_list.append(d)
            for d in pipeline_list:
                owner = d.get('owner','')
                owner_link = f"[[people/{owner}.md]]" if owner else ""
                pipeline_lines.append(f"| {d.get('opportunity','')} | {d.get('status','')} | {owner_link} | {d.get('value','')} | {d.get('jupiterId','')} | {d.get('notes','')} |")
                
            return "# Central Task & Pipeline Board\n\nThis page contains Kamlesh Vyas's work tasks, pending team actions, and active sales pipelines.\n\n---\n\n## 1. Kamlesh Vyas Work Tasks (July 2026)\n\n" + "\n".join(tasks_lines) + "\n\n---\n\n## 2. Pending Actions for the Team\n\n" + "\n".join(action_lines) + "\n\n---\n\n## 3. Pipeline Prospects & Leads\n\n" + "\n".join(pipeline_lines)
        except Exception as e:
            print(f"Firestore get_tasks_context error: {e}")
    return fetch_github_file("brain/tasks.md")

def execute_query(channel, user_text):
    # Fetch key brain context files
    company_context = get_company_context()
    projects_context = get_projects_context()
    tasks_context = get_tasks_context()
    scoreboard_context = get_scoreboard_context()
    
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
