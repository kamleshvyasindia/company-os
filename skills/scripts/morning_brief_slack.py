import csv
import json
import os
import urllib.request
import urllib.parse
from datetime import datetime

# Load env
token = None
env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        for line in f:
            if line.startswith("SLACK_BOT_TOKEN="):
                token = line.split("=")[1].strip()

if not token:
    print("Error: SLACK_BOT_TOKEN not found.")
    exit(1)

channel_id = "C0BFU6N843S"

def post_slack_message(text):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "channel": channel_id,
        "text": text
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            if not res_data.get("ok"):
                print(f"Error posting to Slack: {res_data.get('error')}")
                return False
            print("Successfully posted morning brief to Slack!")
            return True
    except Exception as e:
        print(f"Network error posting to Slack: {e}")
        return False

def generate_brief():
    base_path = os.path.join(os.path.dirname(__file__), "..", "..")
    pending_path = os.path.join(base_path, "Pending Actions  July 2026.csv")
    
    kv_tasks = []
    team_tasks = []
    
    # Get current date formats for today
    today = datetime.now()
    today_formats = [
        today.strftime("%B %d, %Y").lower().strip(),  # "july 04, 2026"
        today.strftime("%B %-d, %Y").lower().strip(),  # "july 4, 2026"
        today.strftime("%b %d, %Y").lower().strip(),   # "jul 04, 2026"
        today.strftime("%b %-d, %Y").lower().strip(),  # "jul 4, 2026"
        today.strftime("%B %d").lower().strip(),       # "july 04"
        today.strftime("%B %-d").lower().strip(),      # "july 4"
        today.strftime("%b %d").lower().strip(),       # "jul 04"
        today.strftime("%b %-d").lower().strip()       # "jul 4"
    ]
    
    # Deduplicate list
    today_formats = list(set(today_formats))
    
    if os.path.exists(pending_path):
        with open(pending_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
        for row in rows[1:]:
            if not row or all(x == '' for x in row):
                continue
            sno, action, who, when, remarks = row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip()
            
            # Check if the task matches any of today's date formats
            when_clean = when.lower().strip()
            is_due_today = any(fmt in when_clean for fmt in today_formats) if when_clean else False
            
            if is_due_today:
                is_kv = "kv" in who.lower() or "kamlesh" in who.lower()
                task_info = f"• *[{who.upper()}]* {action} {f'- _{remarks}_' if remarks else ''}"
                
                if is_kv:
                    kv_tasks.append(task_info)
                else:
                    team_tasks.append(task_info)

    # Format morning brief message
    today_str = today.strftime("%B %-d, %Y")
    message = f"☀️ *Daily Follow-Up Brief ({today_str})* ☀️\n\n"
    
    if not kv_tasks and not team_tasks:
        message += "🟢 *Nothing Due Today!*"
    else:
        if kv_tasks:
            message += "*🔴 Your Tasks (KV) Due Today:*\n" + "\n".join(kv_tasks) + "\n\n"
        if team_tasks:
            message += "*⚠️ Team Tasks Due Today:*\n" + "\n".join(team_tasks) + "\n\n"
            
    message += "_Compiled from your Company OS._"
    return message.strip()

if __name__ == "__main__":
    brief_text = generate_brief()
    post_slack_message(brief_text)
