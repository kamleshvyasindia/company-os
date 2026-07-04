import csv
import json
import os
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

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
    approaching_tasks = []
    
    # Parse Pending Actions
    if os.path.exists(pending_path):
        with open(pending_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
        for row in rows[1:]:
            if not row or all(x == '' for x in row):
                continue
            sno, action, who, when, remarks = row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip()
            
            # Check if owned by KV
            is_kv = "kv" in who.lower() or "kamlesh" in who.lower()
            
            # Check if deadline is approaching
            is_july_15 = "july 15" in when.lower() or "jul 15" in when.lower() or "july 20" in when.lower()
            
            task_info = f"• *[{who.upper()}]* {action} (Target: {when}) {f'- _{remarks}_' if remarks else ''}"
            
            if is_kv:
                kv_tasks.append(task_info)
            elif is_july_15:
                approaching_tasks.append(task_info)

    # Format morning brief message
    today_str = datetime.now().strftime("%B %d, %Y")
    message = f"""☀️ *Good Morning Kamlesh! Here is your Daily Follow-Up Brief ({today_str})* ☀️

🔴 *Your Personal Pending Actions (KV):*
"""
    if kv_tasks:
        message += "\n".join(kv_tasks)
    else:
        message += "• No immediate KV-owned actions listed."
        
    message += """

⚠️ *High Priority Team Actions (Due by July 15-20):*
"""
    if approaching_tasks:
        message += "\n".join(approaching_tasks)
    else:
        message += "• No high priority team actions approaching."
        
    message += """

_This update is automatically compiled from your local Company OS._
"""
    return message.strip()

if __name__ == "__main__":
    brief_text = generate_brief()
    post_slack_message(brief_text)
