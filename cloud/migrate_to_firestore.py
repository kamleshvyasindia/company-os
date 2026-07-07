import os
import re
import json
import firebase_admin
from firebase_admin import credentials, firestore

def clean_wiki_links(text):
    if not text:
        return ""
    # Replace [[people/priyank.md]] with priyank.md or priyank
    match = re.search(r'\[\[(?:people/)?([^\]]+)\]\]', text)
    if match:
        return match.group(1).replace(".md", "")
    return text.strip()

def parse_markdown_table(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    rows = []
    headers = []
    table_started = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|'):
            # Parse row elements
            parts = [p.strip() for p in stripped.split('|')[1:-1]]
            
            # Skip separator line (e.g. | --- | --- |)
            if parts and all(re.match(r'^-+$', p) or p == '' for p in parts):
                continue
                
            if not table_started:
                # First row with contents is header
                headers = parts
                table_started = True
            else:
                # Standard content row
                row_dict = {}
                for idx, part in enumerate(parts):
                    header_name = headers[idx] if idx < len(headers) else f"column_{idx}"
                    row_dict[header_name] = part
                rows.append(row_dict)
        else:
            # Table ended or not started yet
            if table_started and stripped == "":
                # We can reset to allow multiple tables (like in tasks or projects)
                table_started = False
                
    return rows

def run_migration():
    print("Initializing Firebase Admin...")
    
    db = None
    # Look for firebase-key.json in workspace root or cloud folder
    key_paths = [
        "firebase-key.json",
        "cloud/firebase-key.json",
        "../firebase-key.json"
    ]
    
    firebase_key = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY")
    if firebase_key:
        try:
            cred_dict = json.loads(firebase_key)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("Initialized using FIREBASE_SERVICE_ACCOUNT_KEY environment variable.")
        except Exception as e:
            print(f"Failed to initialize using environment variable: {e}")
            
    if not db:
        for path in key_paths:
            if os.path.exists(path):
                try:
                    cred = credentials.Certificate(path)
                    firebase_admin.initialize_app(cred)
                    db = firestore.client()
                    print(f"Initialized using credentials file: {path}")
                    break
                except Exception as e:
                    print(f"Failed to load credentials from {path}: {e}")
                    
    if not db:
        print("\n[ERROR] Firebase could not be initialized.")
        print("Please place your downloaded service account key JSON file at 'cloud/firebase-key.json' or set the 'FIREBASE_SERVICE_ACCOUNT_KEY' environment variable.")
        return

    # 1. Migrate Company Profile
    print("\nMigrating Company Profile...")
    company_path = "brain/company.md"
    if os.path.exists(company_path):
        with open(company_path, 'r', encoding='utf-8') as f:
            content = f.read()
        db.collection("metadata").document("company").set({
            "content": content,
            "updatedAt": firestore.SERVER_TIMESTAMP
        })
        print("Uploaded brain/company.md successfully.")
        
    # 2. Migrate Scoreboard
    print("\nMigrating Scoreboard...")
    scoreboard_path = "scoreboard.md"
    if os.path.exists(scoreboard_path):
        with open(scoreboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
        db.collection("metadata").document("scoreboard").set({
            "content": content,
            "updatedAt": firestore.SERVER_TIMESTAMP
        })
        print("Uploaded scoreboard.md successfully.")

    # 3. Migrate Projects
    print("\nMigrating Projects...")
    projects_path = "brain/projects.md"
    projects = parse_markdown_table(projects_path)
    count = 0
    for proj in projects:
        # Check if it is Table 1 (Government PMU Projects)
        if "WBS Code" in proj:
            wbs = proj.get("WBS Code", "").strip()
            if not wbs or "WBS" in wbs or "wbs" in wbs:
                continue
                
            proj_name = proj.get("Project Name", "").strip()
            if not proj_name:
                continue
                
            doc_id = wbs.replace("/", "_").replace("-", "_").lower()
            if not doc_id or doc_id == "code_awaited":
                doc_id = f"awaited_{count}"
                
            db.collection("projects").document(doc_id).set({
                "wbs": wbs,
                "name": proj_name,
                "client": proj.get("Client", "").strip(),
                "director": clean_wiki_links(proj.get("Project Director (PD)", "")),
                "manager": clean_wiki_links(proj.get("Engagement Manager (EM)", "")),
                "value": proj.get("Value (INR)", "").strip(),
                "monthlyMax": proj.get("Monthly Max (INR)", "").strip(),
                "staffing": proj.get("Deployed / Vacant / Resigned", "").strip(),
                "status": proj.get("Status / Notes", "").strip(),
                "type": "government",
                "updatedAt": firestore.SERVER_TIMESTAMP
            })
            count += 1
            
        # Check if it is Table 2 (Private Sector & AI Training Projects)
        elif "Project Manager" in proj:
            proj_name = proj.get("Project Name", "").strip()
            if not proj_name or "Project Name" in proj_name:
                continue
                
            doc_id = f"private_{proj_name.replace(' ', '_').replace('-', '_').lower()}"
            db.collection("projects").document(doc_id).set({
                "name": proj_name,
                "client": proj.get("Client", "").strip(),
                "manager": clean_wiki_links(proj.get("Project Manager", "")),
                "value": proj.get("Value (INR)", "").strip(),
                "monthlyMax": proj.get("Monthly Max (INR)", "").strip(),
                "deployed": proj.get("Deployed", "").strip(),
                "duration": proj.get("Duration / Timeline", "").strip(),
                "status": proj.get("Status", "").strip(),
                "type": "private",
                "updatedAt": firestore.SERVER_TIMESTAMP
            })
            count += 1
            
    print(f"Uploaded {count} project documents to Firestore.")

    # 4. Migrate Tasks, Team Actions, and Sales Pipelines
    print("\nMigrating Tasks, Team Actions, and Sales Pipelines...")
    tasks_path = "brain/tasks.md"
    all_rows = parse_markdown_table(tasks_path)
    
    task_count = 0
    action_count = 0
    pipeline_count = 0
    
    for r in all_rows:
        # Check if it is Table 1 (Kamlesh Work Tasks)
        if "Event / Meeting" in r:
            event = r.get("Event / Meeting", "").strip()
            if not event or "Event" in event:
                continue
            doc_id = f"task_{task_count}"
            db.collection("tasks").document(doc_id).set({
                "date": r.get("Date", "").strip(),
                "event": event,
                "status": r.get("Status", "").strip(),
                "remarks": r.get("Remarks", "").strip(),
                "updatedAt": firestore.SERVER_TIMESTAMP
            })
            task_count += 1
            
        # Check if it is Table 2 (Pending Team Actions)
        elif "Action Required" in r:
            action = r.get("Action Required", "").strip()
            if not action or "Action" in action:
                continue
            doc_id = f"action_{action_count}"
            db.collection("team_actions").document(doc_id).set({
                "sno": r.get("S.No.", "").strip(),
                "action": action,
                "owner": clean_wiki_links(r.get("Owner", "")),
                "targetDate": r.get("Timeline", "").strip(),
                "status": r.get("Remarks / Status", "").strip(),
                "updatedAt": firestore.SERVER_TIMESTAMP
            })
            action_count += 1
            
        # Check if it is Table 3 (Active Sales Pipeline)
        elif "Opportunity Name" in r:
            opp = r.get("Opportunity Name", "").strip()
            if not opp or "Opportunity" in opp:
                continue
            doc_id = f"pipeline_{pipeline_count}"
            db.collection("pipeline").document(doc_id).set({
                "opportunity": opp,
                "status": r.get("Sales Stage", "").strip(),
                "owner": clean_wiki_links(r.get("Target Owner", "")),
                "value": r.get("Estimated Value (Lakhs)", "").strip(),
                "jupiterId": r.get("Jupiter ID", "").strip(),
                "notes": r.get("Notes", "").strip(),
                "updatedAt": firestore.SERVER_TIMESTAMP
            })
            pipeline_count += 1
            
    print(f"Uploaded {task_count} work task documents to Firestore.")
    print(f"Uploaded {action_count} team action documents to Firestore.")
    print(f"Uploaded {pipeline_count} pipeline prospect documents to Firestore.")
    print("\n[SUCCESS] Migration finished successfully!")

if __name__ == "__main__":
    run_migration()
