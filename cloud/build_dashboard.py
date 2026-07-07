import csv
import json
import os

# Dynamically resolve repository root
script_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(script_dir) if os.path.basename(script_dir) == "cloud" else script_dir

def load_csv(filename):
    file_path = os.path.join(base_path, filename)
    with open(file_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        return list(reader)

def clean_row(row):
    return [col.strip() for col in row]

def parse_employees():
    rows = load_csv("Employees List July 2026.csv")
    headers = clean_row(rows[0])
    data = []
    for r in rows[1:]:
        if not r or all(x == '' for x in r):
            continue
        cleaned = clean_row(r)
        if len(cleaned) < 12:
            cleaned += [''] * (12 - len(cleaned))
        data.append({
            "sno": cleaned[0],
            "id": cleaned[1],
            "name": cleaned[2],
            "designation": cleaned[3],
            "email": cleaned[4],
            "gender": cleaned[5],
            "status": cleaned[6],
            "type": cleaned[7],
            "coach": cleaned[8],
            "project": cleaned[9],
            "wbs": cleaned[10],
            "location": cleaned[11]
        })
    return data

def parse_projects_summary():
    rows = load_csv("Projects summary July 2026.csv")
    data = []
    for r in rows[1:]:
        if not r or all(x == '' for x in r):
            continue
        cleaned = clean_row(r)
        if "106" in cleaned or "22026385.72" in cleaned:
            continue
        if len(cleaned) < 16:
            cleaned += [''] * (16 - len(cleaned))
        data.append({
            "client": cleaned[0],
            "code": cleaned[1],
            "name": cleaned[2],
            "invoicing": cleaned[3],
            "pd": cleaned[4],
            "em": cleaned[5],
            "start": cleaned[6],
            "end": cleaned[7],
            "value": cleaned[8],
            "positions": cleaned[9],
            "max_val": cleaned[10],
            "nsr": cleaned[11],
            "vacant": cleaned[12],
            "resigned": cleaned[13],
            "staffed": cleaned[14],
            "remarks": cleaned[15]
        })
    return data

def parse_other_projects():
    rows = load_csv("Other Projects July 2026.csv")
    data = []
    for r in rows[2:]:
        if not r or all(x == '' for x in r):
            continue
        if "S.No." in r or "Debtirtha" in r[1]:
            break
        cleaned = clean_row(r)
        if len(cleaned) < 11:
            cleaned += [''] * (11 - len(cleaned))
        data.append({
            "sno": cleaned[0],
            "code": cleaned[1],
            "name": cleaned[2],
            "value": cleaned[3],
            "pd": cleaned[4],
            "m_rate": cleaned[5],
            "nsr": cleaned[6],
            "deployed": cleaned[7],
            "start": cleaned[8],
            "end": cleaned[9],
            "duration": cleaned[10]
        })
    return data

def parse_wins():
    rows = load_csv("Wins and Near wins July 2026.csv")
    data = []
    for r in rows[2:]:
        if not r or all(x == '' for x in r):
            continue
        if "Total in INR" in r[1]:
            break
        cleaned = clean_row(r)
        if len(cleaned) < 12:
            cleaned += [''] * (12 - len(cleaned))
        data.append({
            "sno": cleaned[0].replace(".", "").strip(),
            "name": cleaned[1],
            "stage": cleaned[2],
            "amount": cleaned[3],
            "jup_id": cleaned[4],
            "pm": cleaned[5],
            "monthly_val": cleaned[6],
            "start": cleaned[7],
            "duration": cleaned[8],
            "hires": cleaned[9],
            "remarks": cleaned[10],
            "status": cleaned[11]
        })
    return data

def parse_pending_actions():
    rows = load_csv("Pending Actions  July 2026.csv")
    data = []
    for r in rows[1:]:
        if not r or all(x == '' for x in r):
            continue
        cleaned = clean_row(r)
        if len(cleaned) < 5:
            cleaned += [''] * (5 - len(cleaned))
        data.append({
            "sno": cleaned[0],
            "action": cleaned[1],
            "who": cleaned[2],
            "when": cleaned[3],
            "remarks": cleaned[4]
        })
    return data

def parse_personal_tasks():
    rows = load_csv("Kamlesh Vyas Work Tasks  July 2026.csv")
    data = []
    for r in rows[1:]:
        if not r or all(x == '' for x in r):
            continue
        cleaned = clean_row(r)
        if len(cleaned) < 5:
            cleaned += [''] * (5 - len(cleaned))
        data.append({
            "sno": cleaned[0],
            "date": cleaned[1],
            "event": cleaned[2],
            "status": cleaned[3],
            "remarks": cleaned[4]
        })
    return data

def parse_pipeline():
    rows = load_csv("Pipeline prospects  July 2026.csv")
    data = []
    for r in rows[2:]:
        if not r or all(x == '' for x in r):
            continue
        cleaned = clean_row(r)
        if len(cleaned) < 8:
            cleaned += [''] * (8 - len(cleaned))
        if cleaned[1] == '':
            continue
        data.append({
            "sno": cleaned[0],
            "name": cleaned[1],
            "stage": cleaned[2],
            "amount": cleaned[3],
            "jup_id": cleaned[4],
            "pm": cleaned[5],
            "amount_pm": cleaned[6],
            "start": cleaned[7]
        })
    return data

def build():
    employees = parse_employees()
    projects = parse_projects_summary()
    other_projects = parse_other_projects()
    wins = parse_wins()
    pending = parse_pending_actions()
    personal = parse_personal_tasks()
    pipeline = parse_pipeline()
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deloitte India Education Practice - Company OS Dashboard</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-color: #0b0f19;
            --card-bg: rgba(22, 29, 49, 0.7);
            --border-color: rgba(255, 255, 255, 0.08);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-green: #86BC25; /* Deloitte Green */
            --accent-green-hover: #9bd133;
            --shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            --blur: blur(12px);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 24px;
            background-image: 
                radial-gradient(at 10% 10%, rgba(134, 188, 37, 0.08) 0px, transparent 50%),
                radial-gradient(at 90% 90%, rgba(30, 41, 59, 0.5) 0px, transparent 50%);
            background-attachment: fixed;
        }}

        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 28px;
            padding: 20px 32px;
            background: var(--card-bg);
            backdrop-filter: var(--blur);
            -webkit-backdrop-filter: var(--blur);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            box-shadow: var(--shadow);
        }}

        .brand-section {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        .deloitte-dot {{
            width: 14px;
            height: 14px;
            background-color: var(--accent-green);
            border-radius: 50%;
        }}

        .brand-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 24px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}

        .brand-subtitle {{
            font-size: 13px;
            color: var(--text-secondary);
            margin-top: 2px;
        }}

        /* Grid Layout */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 28px;
        }}

        .kpi-card {{
            background: var(--card-bg);
            backdrop-filter: var(--blur);
            -webkit-backdrop-filter: var(--blur);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 24px;
            box-shadow: var(--shadow);
            transition: transform 0.2s, border-color 0.2s;
        }}

        .kpi-card:hover {{
            transform: translateY(-4px);
            border-color: rgba(134, 188, 37, 0.3);
        }}

        .kpi-label {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-secondary);
            margin-bottom: 12px;
            font-weight: 600;
        }}

        .kpi-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 32px;
            font-weight: 700;
            color: var(--text-primary);
        }}

        .kpi-sub {{
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 6px;
        }}

        .dashboard-container {{
            display: grid;
            grid-template-columns: 260px 1fr;
            gap: 28px;
        }}

        /* Sidebar Navigation */
        .side-menu {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .menu-btn {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            padding: 16px 20px;
            border-radius: 14px;
            font-size: 14px;
            font-weight: 600;
            text-align: left;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .menu-btn:hover {{
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-primary);
            border-color: rgba(134, 188, 37, 0.2);
        }}

        .menu-btn.active {{
            background: var(--accent-green);
            color: #000;
            border-color: var(--accent-green);
            box-shadow: 0 4px 20px 0 rgba(134, 188, 37, 0.3);
        }}

        /* Content Panel */
        .main-panel {{
            background: var(--card-bg);
            backdrop-filter: var(--blur);
            -webkit-backdrop-filter: var(--blur);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 28px;
            box-shadow: var(--shadow);
            min-height: 500px;
        }}

        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
            display: block;
        }}

        .panel-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }}

        .panel-title {{
            font-size: 20px;
            color: var(--text-primary);
        }}

        /* Search / Filters */
        .filter-bar {{
            display: flex;
            gap: 16px;
            margin-bottom: 20px;
        }}

        .search-input, .select-input {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 10px 16px;
            border-radius: 10px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
        }}

        .search-input {{
            flex: 1;
        }}

        .search-input:focus, .select-input:focus {{
            border-color: var(--accent-green);
        }}

        /* Tables styling */
        .table-container {{
            overflow-x: auto;
            margin-bottom: 20px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
            text-align: left;
        }}

        th {{
            background: rgba(255, 255, 255, 0.02);
            color: var(--text-secondary);
            font-weight: 600;
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-color);
        }}

        td {{
            padding: 14px 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            color: var(--text-primary);
        }}

        tr:hover {{
            background: rgba(255, 255, 255, 0.02);
        }}

        /* Badges */
        .badge {{
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            display: inline-block;
            text-transform: uppercase;
        }}

        .badge-active {{
            background: rgba(134, 188, 37, 0.15);
            color: var(--accent-green);
        }}

        .badge-done {{
            background: rgba(134, 188, 37, 0.15);
            color: var(--accent-green);
        }}

        .badge-pending {{
            background: rgba(245, 158, 11, 0.15);
            color: #f59e0b;
        }}

        .badge-resigned {{
            background: rgba(239, 68, 68, 0.15);
            color: #ef4444;
        }}

        /* Chart container */
        .charts-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
        }}

        .chart-box {{
            background: rgba(255, 255, 255, 0.01);
            border: 1px solid rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            padding: 20px;
        }}

        .chart-box h4 {{
            font-size: 14px;
            color: var(--text-secondary);
            margin-bottom: 16px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        /* Custom Gauge Graphic */
        .gauge-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 180px;
        }}

        .gauge-val {{
            font-size: 36px;
            font-weight: 700;
            color: var(--accent-green);
        }}

        .gauge-lbl {{
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 8px;
        }}
    </style>
</head>
<body>

    <header>
        <div class="brand-section">
            <span class="deloitte-dot"></span>
            <div>
                <h1 class="brand-title">Deloitte. <span style="font-weight: 300;">Education Practice</span></h1>
                <p class="brand-subtitle">Company OS Dashboard — July 2026</p>
            </div>
        </div>
        <div>
            <span class="badge badge-active" style="padding: 6px 12px; font-size: 12px;">Active System</span>
        </div>
    </header>

    <!-- KPI Section -->
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Monthly revenue (NSR)</div>
            <div class="kpi-value">₹2.71 Cr</div>
            <div class="kpi-sub">₹2.20 Cr Govt + ₹50.8L Private</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Active projects</div>
            <div class="kpi-value">25</div>
            <div class="kpi-sub">20 Govt PMUs + 5 Private/AI</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Hiring vacancies</div>
            <div class="kpi-value">13</div>
            <div class="kpi-sub">106 total roles (89 filled, 4 resigned)</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">AI wins (90-Day Target)</div>
            <div class="kpi-value">₹1.62 Cr <span style="font-size: 18px; color: var(--text-secondary);">/ ₹5Cr</span></div>
            <div class="kpi-sub">32.4% of target met</div>
        </div>
    </div>

    <!-- Main Section -->
    <div class="dashboard-container">
        <!-- Sidebar Navigation -->
        <div class="side-menu">
            <button class="menu-btn active" onclick="switchTab('overview')">📊 Overview / Metrics</button>
            <button class="menu-btn" onclick="switchTab('projects')">📁 Active Projects</button>
            <button class="menu-btn" onclick="switchTab('team')">👥 Team Directory</button>
            <button class="menu-btn" onclick="switchTab('wins')">🏆 Wins & Near Wins</button>
            <button class="menu-btn" onclick="switchTab('tasks')">📋 Tasks & Action Items</button>
        </div>

        <!-- Main Panel -->
        <div class="main-panel">
            <!-- 1. Overview Tab -->
            <div id="overview" class="tab-content active">
                <div class="panel-header">
                    <h2 class="panel-title">Overview & Performance Metrics</h2>
                </div>
                <div class="charts-container">
                    <div class="chart-box">
                        <h4>Staffing Distribution (Govt PMUs)</h4>
                        <canvas id="staffingChart"></canvas>
                    </div>
                    <div class="chart-box">
                        <h4>90-Day AI Revenue Target Gauge</h4>
                        <div class="gauge-container">
                            <div class="gauge-val">32.4%</div>
                            <div style="font-size: 18px; font-weight:600; margin-top:4px;">₹1.62 Crore / ₹5 Crore</div>
                            <div class="gauge-lbl">Google workshops (₹40L), ICICI AI (₹10L), & UNeXT AI (₹1.12 Cr)</div>
                        </div>
                    </div>
                </div>
                <div class="charts-container" style="margin-top: 24px;">
                    <div class="chart-box" style="grid-column: span 2;">
                        <h4>Monthly NSR Contribution by Segment</h4>
                        <canvas id="revenueChart" style="max-height: 220px;"></canvas>
                    </div>
                </div>
            </div>

            <!-- 2. Projects Tab -->
            <div id="projects" class="tab-content">
                <div class="panel-header">
                    <h2 class="panel-title">Government PMUs & Active Projects</h2>
                    <input type="text" id="projectSearch" class="search-input" placeholder="Search by Project or Client..." onkeyup="filterProjects()">
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>WBS Code</th>
                                <th>Client Name</th>
                                <th>Project Name</th>
                                <th>PD</th>
                                <th>EM</th>
                                <th>Value</th>
                                <th>NSR/mo</th>
                                <th>Deployed</th>
                            </tr>
                        </thead>
                        <tbody id="projectsTableBody">
                            <!-- Dynamic Content -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- 3. Team Tab -->
            <div id="team" class="tab-content">
                <div class="panel-header">
                    <h2 class="panel-title">Employee Directory</h2>
                    <div class="filter-bar">
                        <input type="text" id="teamSearch" class="search-input" placeholder="Search by Name, Role, or Coach..." onkeyup="filterTeam()">
                        <select id="teamLocationFilter" class="select-input" onchange="filterTeam()">
                            <option value="all">All Locations</option>
                            <option value="Delhi">Delhi</option>
                            <option value="Punjab">Punjab</option>
                            <option value="Gujarat">Gujarat</option>
                            <option value="UP">UP</option>
                            <option value="Bangalore">Bangalore</option>
                        </select>
                    </div>
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Employee Name</th>
                                <th>Designation</th>
                                <th>Coach</th>
                                <th>Project / Account</th>
                                <th>Location</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody id="teamTableBody">
                            <!-- Dynamic Content -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- 4. Wins Tab -->
            <div id="wins" class="tab-content">
                <div class="panel-header">
                    <h2 class="panel-title">Wins & Near Wins Pipeline</h2>
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Deal Name</th>
                                <th>Stage</th>
                                <th>Total Fee</th>
                                <th>Project Manager</th>
                                <th>New Hires</th>
                                <th>Start Date</th>
                            </tr>
                        </thead>
                        <tbody id="winsTableBody">
                            <!-- Dynamic Content -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- 5. Tasks Tab -->
            <div id="tasks" class="tab-content">
                <div class="panel-header">
                    <h2 class="panel-title">Task Management Board</h2>
                    <select id="actionOwnerFilter" class="select-input" onchange="filterActions()">
                        <option value="all">All Owners</option>
                        <option value="kv">Kamlesh Vyas (KV)</option>
                        <option value="mansi">Mansi</option>
                        <option value="rajat">Rajat</option>
                        <option value="deependra">Deependra</option>
                        <option value="arvind">Arvind</option>
                        <option value="priyank">Priyank</option>
                        <option value="bhavisha">Bhavisha</option>
                        <option value="meethi">Meethi</option>
                        <option value="harshit">Harshit</option>
                    </select>
                </div>
                
                <h3 style="font-size:15px; margin-bottom:12px; color: var(--accent-green); text-transform:uppercase; letter-spacing:0.5px;">1. KV Personal Schedule</h3>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Meeting / Event</th>
                                <th>Status</th>
                                <th>Remarks</th>
                            </tr>
                        </thead>
                        <tbody id="personalTasksTableBody">
                            <!-- Dynamic Content -->
                        </tbody>
                    </table>
                </div>

                <h3 style="font-size:15px; margin-top:28px; margin-bottom:12px; color: var(--accent-green); text-transform:uppercase; letter-spacing:0.5px;">2. Team Pending Action List</h3>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>S.No.</th>
                                <th>Action Required</th>
                                <th>Owner</th>
                                <th>Timeline</th>
                                <th>Remarks</th>
                            </tr>
                        </thead>
                        <tbody id="actionsTableBody">
                            <!-- Dynamic Content -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- Data Injection & Init Scripts -->
    <script>
        const employeesData = {json.dumps(employees)};
        const projectsData = {json.dumps(projects)};
        const otherProjectsData = {json.dumps(other_projects)};
        const winsData = {json.dumps(wins)};
        const pendingActionsData = {json.dumps(pending)};
        const personalTasksData = {json.dumps(personal)};

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.menu-btn').forEach(el => el.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }}

        function initDashboard() {{
            // Populate Projects
            const projBody = document.getElementById('projectsTableBody');
            projectsData.forEach(p => {{
                const row = document.createElement('tr');
                row.setAttribute('data-name', p.name.toLowerCase());
                row.setAttribute('data-client', p.client.toLowerCase());
                row.innerHTML = `
                    <td><code>${{p.code}}</code></td>
                    <td><strong>${{p.client}}</strong></td>
                    <td style="color: var(--accent-green);">${{p.name}}</td>
                    <td>${{p.pd}}</td>
                    <td>${{p.em}}</td>
                    <td>₹${{p.value}} L</td>
                    <td>₹${{p.nsr}} L</td>
                    <td>${{p.staffed}} / ${{p.vacant}}</td>
                `;
                projBody.appendChild(row);
            }});

            // Populate Team
            const teamBody = document.getElementById('teamTableBody');
            employeesData.forEach(e => {{
                const row = document.createElement('tr');
                row.setAttribute('data-name', e.name.toLowerCase());
                row.setAttribute('data-desig', e.designation.toLowerCase());
                row.setAttribute('data-coach', e.coach.toLowerCase());
                row.setAttribute('data-location', e.location);
                
                let badgeClass = 'badge-active';
                if (e.status.toLowerCase().includes('resigned')) badgeClass = 'badge-resigned';
                
                row.innerHTML = `
                    <td>${{e.id}}</td>
                    <td><strong>${{e.name}}</strong></td>
                    <td>${{e.designation}}</td>
                    <td>${{e.coach || '—'}}</td>
                    <td style="color: var(--text-secondary);">${{e.project || '—'}}</td>
                    <td>${{e.location}}</td>
                    <td><span class="badge ${{badgeClass}}">${{e.status}}</span></td>
                `;
                teamBody.appendChild(row);
            }});

            // Populate Wins
            const winsBody = document.getElementById('winsTableBody');
            winsData.forEach(w => {{
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><strong>${{w.name}}</strong></td>
                    <td><span class="badge badge-active">${{w.stage}}</span></td>
                    <td style="font-weight:600; color: var(--accent-green);">₹${{w.amount}} Lakhs</td>
                    <td>${{w.pm}}</td>
                    <td>${{w.hires || '—'}}</td>
                    <td>${{w.start}}</td>
                `;
                winsBody.appendChild(row);
            }});

            // Populate Pending Actions
            const actionsBody = document.getElementById('actionsTableBody');
            pendingActionsData.forEach(a => {{
                const row = document.createElement('tr');
                row.setAttribute('data-owner', a.who.toLowerCase());
                row.innerHTML = `
                    <td>${{a.sno}}</td>
                    <td><strong>${{a.action}}</strong></td>
                    <td style="color: var(--accent-green);">${{a.who}}</td>
                    <td>${{a.when || 'ASAP'}}</td>
                    <td style="color: var(--text-secondary);">${{a.remarks}}</td>
                `;
                actionsBody.appendChild(row);
            }});

            // Populate Personal Tasks
            const personalBody = document.getElementById('personalTasksTableBody');
            personalTasksData.forEach(t => {{
                const row = document.createElement('tr');
                let badgeClass = t.status.toLowerCase().includes('done') ? 'badge-done' : 'badge-pending';
                row.innerHTML = `
                    <td>${{t.date}}</td>
                    <td><strong>${{t.event}}</strong></td>
                    <td><span class="badge ${{badgeClass}}">${{t.status}}</span></td>
                    <td style="color: var(--text-secondary);">${{t.remarks || '—'}}</td>
                `;
                personalBody.appendChild(row);
            }});

            initCharts();
        }}

        function filterProjects() {{
            const search = document.getElementById('projectSearch').value.toLowerCase();
            document.querySelectorAll('#projectsTableBody tr').forEach(row => {{
                const name = row.getAttribute('data-name');
                const client = row.getAttribute('data-client');
                if (name.includes(search) || client.includes(search)) {{
                    row.style.display = '';
                }} else {{
                    row.style.display = 'none';
                }}
            }});
        }}

        function filterTeam() {{
            const search = document.getElementById('teamSearch').value.toLowerCase();
            const location = document.getElementById('teamLocationFilter').value;
            
            document.querySelectorAll('#teamTableBody tr').forEach(row => {{
                const name = row.getAttribute('data-name');
                const desig = row.getAttribute('data-desig');
                const coach = row.getAttribute('data-coach');
                const rowLoc = row.getAttribute('data-location');
                
                const matchesSearch = name.includes(search) || desig.includes(search) || coach.includes(search);
                const matchesLoc = location === 'all' || rowLoc === location;
                
                if (matchesSearch && matchesLoc) {{
                    row.style.display = '';
                }} else {{
                    row.style.display = 'none';
                }}
            }});
        }}

        function filterActions() {{
            const owner = document.getElementById('actionOwnerFilter').value;
            document.querySelectorAll('#actionsTableBody tr').forEach(row => {{
                const rowOwner = row.getAttribute('data-owner');
                const matchesOwner = owner === 'all' || 
                                     (owner === 'kv' && (rowOwner === 'kv' || rowOwner === 'kamlesh vyas')) ||
                                     rowOwner.includes(owner);
                if (matchesOwner) {{
                    row.style.display = '';
                }} else {{
                    row.style.display = 'none';
                }}
            }});
        }}

        let staffingChart, revenueChart;

        function initCharts() {{
            const ctxStaff = document.getElementById('staffingChart').getContext('2d');
            staffingChart = new Chart(ctxStaff, {{
                type: 'doughnut',
                data: {{
                    labels: ['Staffed Roles', 'Vacant Positions', 'Resigned (Pending replacement)'],
                    datasets: [{{
                        data: [89, 13, 4],
                        backgroundColor: [
                            'rgba(134, 188, 37, 0.8)',
                            'rgba(245, 158, 11, 0.8)',
                            'rgba(239, 68, 68, 0.8)'
                        ],
                        borderColor: [
                            '#86BC25',
                            '#f59e0b',
                            '#ef4444'
                        ],
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{
                            position: 'bottom',
                            labels: {{
                                color: '#94a3b8',
                                padding: 16
                            }}
                        }}
                    }}
                }}
            }});

            const ctxRev = document.getElementById('revenueChart').getContext('2d');
            revenueChart = new Chart(ctxRev, {{
                type: 'bar',
                data: {{
                    labels: ['Gujarat PMUs', 'NCERT/Delhi PMUs', 'Punjab PMUs', 'UP PMUs', 'Private AI (Google/ICICI/UNeXT)'],
                    datasets: [{{
                        label: 'Monthly Net Sales Rate (NSR) in Lakhs',
                        data: [134.62, 38.96, 33.54, 25.33, 42.00],
                        backgroundColor: 'rgba(134, 188, 37, 0.8)',
                        borderColor: '#86BC25',
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            grid: {{
                                color: 'rgba(255, 255, 255, 0.05)'
                            }},
                            ticks: {{
                                color: '#94a3b8'
                            }}
                        }},
                        x: {{
                            grid: {{
                                display: false
                            }},
                            ticks: {{
                                color: '#94a3b8'
                            }}
                        }}
                    }},
                    plugins: {{
                        legend: {{
                            display: false
                        }}
                    }}
                }}
            }});
        }}

        window.onload = initDashboard;
    </script>
</body>
</html>
"""
    
    target_dashboard_html = os.path.join(base_path, "dashboard.html")
    with open(target_dashboard_html, "w", encoding="utf-8") as f:
        f.write(html_template)
    print("Generated dashboard.html successfully!")

if __name__ == "__main__":
    build()
