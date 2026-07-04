import csv
import os

base_path = "/Users/kamleshvyas/Documents/outskill 2026/company_os"

def update_pending_actions():
    pending_path = os.path.join(base_path, "Pending Actions  July 2026.csv")
    
    headers = ['S, No. ', 'Actions ', 'Who', 'When ', 'Remarks ']
    actions_data = [
        ["1", "Harshit contract and first invoice request and payment", "Mansi", "July 15, 2026", "for May and June"],
        ["2", "CL engagement for 2 persons", "Rajat", "August 10, 2026", ""],
        ["3", "Akhil engagement", "Mansi", "August 10, 2026", ""],
        ["4", "Code generation and invoicing for CAG", "Deependra", "July 15, 2026", ""],
        ["5", "Code generation and invoicing for Bharat Innovates", "Deependra", "July 15, 2026", ""],
        ["6", "Deployment, Code generation and invoicing for University Township", "Rajat / Arvind", "July 15, 2026", ""],
        ["7", "Deployment, Code generation and invoicing for PMRC", "Rajat", "August 15, 2026", ""],
        ["8", "Code generation and invoicing for ADB green Jobs (Individual Consultants)", "Manish", "July 15, 2026", ""],
        ["9", "Niti closure", "Mansi", "August 10, 2026", ""],
        ["10", "GMR final invoice", "Deependra", "August 10, 2026", ""],
        ["11", "ICICI invoice", "Rajat", "July 15, 2026", ""],
        ["12", "GSDM WO and deployment", "Priyank", "August 10, 2026", ""],
        ["13", "DGSE extention and deployment", "Bhavisha", "August 10, 2026", ""],
        ["14", "IIIT Jammu WO", "KV", "July 15, 2026", ""],
        ["15", "MNIT (IIIT Kota) WO and invoice", "KV", "August 10, 2026", "follow up Prof Padhy July 15"],
        ["16", "Sachin/ Sid Ashwin EMeritus", "KV", "August 15, 2026", ""],
        ["17", "AMLI", "KV", "August 15, 2026", "Next follow up on July 20 to study LMS"],
        ["18", "Jain Univ", "KV", "July 15, 2026", "Need to send proposal"],
        ["19", "AI for school Leaders - CII", "KV", "July 15, 2026", "Need to send outline"],
        ["20", "English Hackathon Punjab", "KV / Meethi", "August 15, 2026", ""],
        ["21", "Haryana Counselling", "Meethi", "August 15, 2026", ""],
        ["22", "Prof Ajay Sharma Gurugram Univ article", "Mansi", "July 15, 2026", ""],
        ["23", "UPES", "Samanvay", "August 10, 2026", ""],
        ["24", "Edtech- BMU, Times", "Deb", "August 10, 2026", ""],
        ["25", "UNSW", "Deb", "August 10, 2026", ""],
        ["26", "ABES", "KV", "August 10, 2026", ""],
        ["27", "Google workshops and overall agreement", "KV", "July 15, 2026", ""],
        ["28", "SGT", "KV", "August 10, 2026", ""],
        ["29", "Army workshop", "KV", "August 10, 2026", ""],
        ["30", "Amity- south Africa, studies, AI workshop, Maldives", "KV", "August 10, 2026", ""],
        ["31", "Renew", "KV", "August 10, 2026", ""],
        ["32", "Karnataka Higher Ed", "Priyank", "August 10, 2026", ""],
        ["33", "MP Higher Ed", "Meethi / Deependra", "August 10, 2026", ""],
        ["34", "UP AI", "Arvind", "July 15, 2026", ""],
        ["35", "VBU", "KV", "August 10, 2026", ""],
        ["36", "UP Hiring", "Arvind", "August 10, 2026", ""],
        ["37", "Study AMLI LMS system & pitch Simulation/Content ideas", "Harshit", "July 20, 2026", "Meeting held on July 2 (Retained old task)"]
    ]
    
    with open(pending_path, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(actions_data)
    print("Pending Actions CSV updated with 37 tasks successfully!")

def update_wins_and_pipeline():
    wins_path = os.path.join(base_path, "Wins and Near wins July 2026.csv")
    rows = []
    with open(wins_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
    # Find insertion point (just before the total row, which is the last row)
    insert_idx = -1
    for i, r in enumerate(rows):
        if len(r) > 1 and "total in inr" in r[1].lower():
            insert_idx = i
            break
            
    if insert_idx == -1:
        insert_idx = len(rows)
        
    new_win = [
        "16", 
        "GSBTM PMU, Gujarat", 
        "Won", 
        "84", 
        "", 
        "Priyank Patel", 
        "7", 
        "August 1, 2026", 
        "12 months", 
        "2", 
        "Gujarat State Bio Tech Mission", 
        "Avinash as EM", 
        ""
    ]
    
    rows.insert(insert_idx, new_win)
    
    # Recalculate Total
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
    print(f"New Total Win Value: {total_val} Lakhs")
    
    with open(wins_path, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
        
    print("Wins and Near Wins CSV updated with GSBTM win successfully!")

if __name__ == "__main__":
    update_pending_actions()
    update_wins_and_pipeline()
