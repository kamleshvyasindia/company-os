import csv
import os

# Dynamically resolve repository root
script_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(script_dir) if os.path.basename(script_dir) == "cloud" else script_dir

def load_csv(filename):
    file_path = os.path.join(base_path, filename)
    with open(file_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        return list(reader)

def generate_projects_md():
    projects_summary = load_csv("Projects summary July 2026.csv")
    other_projects = load_csv("Other Projects July 2026.csv")
    
    projects_content = """# Active Projects Directory

This directory lists all active education and skills engagements across government and private sector clients.

---

## Government PMU Projects

| WBS Code | Project Name | Client | Project Director (PD) | Engagement Manager (EM) | Value (INR) | Monthly Max (INR) | Deployed / Vacant / Resigned | Status / Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
"""
    
    for row in projects_summary[1:]:
        if not row or all(x == '' for x in row):
            continue
        if "106" in row or "22026385.72" in row:
            continue
        client = row[0].strip()
        wbs = row[1].strip()
        proj_name = row[2].strip()
        invoicing = row[3].strip()
        pd = row[4].strip()
        em = row[5].strip()
        val = row[8].strip()
        max_val = row[10].strip()
        nsr = row[11].strip()
        vacant = row[12].strip()
        resigned = row[13].strip()
        staffed = row[14].strip()
        remarks = row[15].strip()
        
        pd_link = f"[[people/priyank.md]]" if "priyank" in pd.lower() else (
                  f"[[people/deependra.md]]" if "deependra" in pd.lower() else (
                  f"[[people/arvind.md]]" if "arvind" in pd.lower() else (
                  f"[[people/rajat.md]]" if "rajat" in pd.lower() else (
                  f"[[people/bhavisha.md]]" if "bhavisha" in pd.lower() else (
                  f"[[people/meethi.md]]" if "meethi" in pd.lower() else pd)))))
                  
        em_link = f"[[people/gaurav_mathur.md]]" if "gaurav" in em.lower() else (
                  f"[[people/ved_gupta.md]]" if "ved" in em.lower() else (
                  f"[[people/priyank.md]]" if "priyank" in em.lower() else (
                  f"[[people/rajat.md]]" if "rajat" in em.lower() else (
                  f"[[people/bhavisha.md]]" if "bhavisha" in em.lower() else (
                  f"[[people/meethi.md]]" if "meethi" in em.lower() else em)))))

        projects_content += f"| `{wbs}` | {proj_name} | {client} | {pd_link} | {em_link} | ₹{val} | ₹{max_val} | {staffed} / {vacant} / {resigned} | Invoicing: {invoicing}. {remarks} |\n"

    projects_content += """
---

## Private Sector & AI Training Projects

| Project Name | Client | Project Manager | Value (INR) | Monthly Max (INR) | Deployed | Duration / Timeline | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
"""

    for row in other_projects[2:]:
        if not row or all(x == '' for x in row):
            continue
        if "S.No." in row or "Debtirtha" in row[1]:
            break
        code = row[1].strip()
        name = row[2].strip()
        val = row[3].strip()
        m_rate = row[5].strip()
        deployed = row[7].strip()
        start = row[8].strip()
        end = row[9].strip()
        dur = row[10].strip()
        
        deployed_link = f"[[people/deb.md]]" if "debtirtha" in deployed.lower() or "deb" in deployed.lower() else deployed
        projects_content += f"| {name} | Private Partner | {deployed_link} | ₹{val} | ₹{m_rate} | 1 | {start} to {end} ({dur} mos) | Code: {code} |\n"

    target_projects_md = os.path.join(base_path, "brain", "projects.md")
    with open(target_projects_md, "w", encoding="utf-8") as f:
        f.write(projects_content)
    print("Generated projects.md successfully!")

def generate_tasks_md():
    tasks = load_csv("Kamlesh Vyas Work Tasks  July 2026.csv")
    pending = load_csv("Pending Actions  July 2026.csv")
    pipeline = load_csv("Pipeline prospects  July 2026.csv")
    
    tasks_content = """# Central Task & Pipeline Board

This page contains Kamlesh Vyas's work tasks, pending team actions, and active sales pipelines.

---

## 1. Kamlesh Vyas Work Tasks (July 2026)

| Date | Event / Meeting | Status | Remarks |
| --- | --- | --- | --- |
"""

    for row in tasks[1:]:
        if not row or all(x == '' for x in row):
            continue
        sno = row[0].strip()
        date = row[1].strip()
        event = row[2].strip()
        status = row[3].strip()
        remarks = row[4].strip()
        status_box = "✅ Done" if "done" in status.lower() else "⏳ Pending"
        tasks_content += f"| {date} | {event} | {status_box} | {remarks} |\n"

    tasks_content += """
---

## 2. Pending Actions for the Team

| S.No. | Action Required | Owner | Timeline | Remarks / Status |
| --- | --- | --- | --- | --- |
"""

    for row in pending[1:]:
        if not row or all(x == '' for x in row):
            continue
        sno = row[0].strip()
        action = row[1].strip()
        who = row[2].strip()
        when = row[3].strip()
        remarks = row[4].strip()
        
        who_link = f"[[people/deb.md]]" if "deb" in who.lower() else (
                   f"[[people/priyank.md]]" if "priyank" in who.lower() else (
                   f"[[people/deependra.md]]" if "deependra" in who.lower() else (
                   f"[[people/arvind.md]]" if "arvind" in who.lower() else (
                   f"[[people/rajat.md]]" if "rajat" in who.lower() else (
                   f"[[people/meethi.md]]" if "meethi" in who.lower() else (
                   f"[[people/bhavisha.md]]" if "bhavisha" in who.lower() else (
                   f"[[people/kamlesh.md]]" if who.lower() == "kv" else who)))))))

        tasks_content += f"| {sno} | {action} | {who_link} | {when or 'ASAP'} | {remarks} |\n"

    tasks_content += """
---

## 3. Pipeline Prospects & Leads

| Opportunity Name | Sales Stage | Target Owner | Estimated Value (Lakhs) | Jupiter ID | Notes |
| --- | --- | --- | --- | --- | --- |
"""

    for row in pipeline[1:]:
        if not row or all(x == '' for x in row):
            continue
        if "Edtech- BMU" in row[1] or "Edtech-" in row[1] or row[1].strip() == '':
            if row[1].strip() == '':
                continue
        sno = row[0].strip()
        name = row[1].strip()
        stage = row[2].strip()
        val = row[3].strip()
        jup_id = row[4].strip()
        pm = row[5].strip()
        pm_val = row[6].strip()
        start = row[7].strip()
        
        pm_link = f"[[people/deb.md]]" if "deb" in pm.lower() else (
                  f"[[people/kamlesh.md]]" if "kv" in pm.lower() else (
                  f"[[people/arvind.md]]" if "arvind" in pm.lower() else pm))

        tasks_content += f"| {name} | {stage or 'Prospect'} | {pm_link} | ₹{val or 'TBD'} L | {jup_id or 'TBD'} | PM Value: {pm_val or 'TBD'}, Start: {start or 'TBD'} |\n"

    target_tasks_md = os.path.join(base_path, "brain", "tasks.md")
    with open(target_tasks_md, "w", encoding="utf-8") as f:
        f.write(tasks_content)
    print("Generated tasks.md successfully!")

if __name__ == "__main__":
    generate_projects_md()
    generate_tasks_md()
