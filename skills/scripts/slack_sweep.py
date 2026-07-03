import json
import os
import urllib.request
import urllib.parse
from datetime import datetime

# Load environment variables
token = None
env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        for line in f:
            if line.startswith("SLACK_BOT_TOKEN="):
                token = line.split("=")[1].strip()

if not token:
    print("Error: SLACK_BOT_TOKEN not found in .env file.")
    exit(1)

channel_name = "deloitte-education"
channel_id = "C0BFU6N843S"
inbox_dir = os.path.join(os.path.dirname(__file__), "..", "..", "inbox")
os.makedirs(inbox_dir, exist_ok=True)

def slack_api_call(method, params=None):
    url = f"https://slack.com/api/{method}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = None
    if params:
        data = urllib.parse.urlencode(params).encode("utf-8")
        
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            if not res_data.get("ok"):
                print(f"Slack API error in {method}: {res_data.get('error')}")
                return None
            return res_data
    except Exception as e:
        print(f"Network error calling Slack API {method}: {e}")
        return None

def sweep_messages():
    print(f"Connecting to channel '#{channel_name}' using hardcoded ID: {channel_id}")
    
    # Fetch history
    res = slack_api_call("conversations.history", {"channel": channel_id, "limit": 20})
    if not res:
        return
        
    messages = res.get("messages", [])
    print(f"Fetched {len(messages)} messages.")
    
    swept_count = 0
    for msg in messages:
        # Skip bot messages
        if msg.get("bot_id") or msg.get("subtype") == "bot_message":
            continue
            
        ts = float(msg.get("ts", 0))
        dt = datetime.fromtimestamp(ts)
        timestamp_str = dt.strftime("%Y-%m-%d-%H%M%S")
        
        # Check if we already swept this message by checking if a file with this timestamp exists in inbox
        filename = f"{timestamp_str}-slack-capture.md"
        filepath = os.path.join(inbox_dir, filename)
        
        if os.path.exists(filepath):
            continue
            
        text = msg.get("text", "")
        user = msg.get("user", "UnknownUser")
        
        # Write message to inbox
        content = f"""# Slack Capture — {dt.strftime("%Y-%m-%d %H:%M:%S")}
- **Channel:** #{channel_name} ({channel_id})
- **User:** {user}
- **Timestamp:** {msg.get("ts")}

---

{text}
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Swept message to: {filename}")
        swept_count += 1
        
    print(f"Successfully swept {swept_count} new messages into inbox/.")

if __name__ == "__main__":
    sweep_messages()
