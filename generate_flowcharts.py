"""
Generate visual SVG flowcharts for each of the 10 Case Studies.
"""
import os

FLOWCHARTS = {
    "Case_Study_02_Electricity_Billing": {
        "title": "Case 02: Progressive Electricity Billing Flowchart",
        "nodes": [
            ("Start", "Start: Read Monthly Consumption", "oval", "#3b82f6"),
            ("Loop", "For Each Month (U units)", "rect", "#6366f1"),
            ("Tiers", "Compute Slab Charges (Slab 1..4)", "rect", "#8b5cf6"),
            ("Fixed", "Subtotal = Energy + Fixed Meter (₹75)", "rect", "#8b5cf6"),
            ("Surch", "Subtotal > ₹1500 ? Add 5% Surcharge", "diamond", "#ec4899"),
            ("Rebate", "U <= 150 ? Apply 3% Green Rebate", "diamond", "#ec4899"),
            ("Anomaly", "Compare with Prev Month (|Δ| >= 30%)", "diamond", "#f59e0b"),
            ("Pack", "Append Result Tuple to Bills List", "rect", "#10b981"),
            ("End", "Display Formatted Invoice & End", "oval", "#3b82f6")
        ]
    },
    "Case_Study_26_Seating_Arrangement": {
        "title": "Case 26: Seating Arrangement Generator Flowchart",
        "nodes": [
            ("Start", "Start: Input R x C & Student Pool", "oval", "#3b82f6"),
            ("Init", "Initialize R x C Grid with [VACANT]", "rect", "#6366f1"),
            ("Reserve", "Mark Reserved Seats (PWD, Buffer)", "rect", "#8b5cf6"),
            ("LoopR", "Nested Loop: Row r in 0..R-1", "rect", "#6366f1"),
            ("LoopC", "Nested Loop: Col c in 0..C-1", "rect", "#6366f1"),
            ("CheckAdj", "Does Candidate Match Neighbors' Dept?", "diamond", "#ec4899"),
            ("Place", "Assign Seat: [DEPT-ROLL] & Pop Candidate", "rect", "#10b981"),
            ("Buffer", "If Conflict: Mark Desk as [BUFFER]", "rect", "#f59e0b"),
            ("End", "Display Hall Map & Audit -> End", "oval", "#3b82f6")
        ]
    },
    "Case_Study_27_Pattern_Generator": {
        "title": "Case 27: Advanced Numeric Pattern Flowchart",
        "nodes": [
            ("Start", "Start: Input Dimension N", "oval", "#3b82f6"),
            ("Valid", "Validate N: Odd, 3 <= N <= 25", "diamond", "#ec4899"),
            ("Error", "If Invalid: Display Error & Exit", "rect", "#ef4444"),
            ("Mid", "Compute Midpoint = N // 2", "rect", "#6366f1"),
            ("Upper", "Nested Loop: Upper Diamond (Spaces & Numbers)", "rect", "#8b5cf6"),
            ("Waist", "Render Central Waist Row", "rect", "#8b5cf6"),
            ("Lower", "Nested Loop: Lower Symmetrical Reflection", "rect", "#8b5cf6"),
            ("Palind", "Render Multi-layer Palindromic Pyramid", "rect", "#10b981"),
            ("End", "Render Monospace Pattern Suite -> End", "oval", "#3b82f6")
        ]
    },
    "Case_Study_31_Answer_Key_Evaluator": {
        "title": "Case 31: Answer Key Evaluator Flowchart",
        "nodes": [
            ("Start", "Start: Ingest Answer Key & Student Answers", "oval", "#3b82f6"),
            ("Validate", "Validate String Length & Chars (A,B,C,D,X)", "diamond", "#ec4899"),
            ("LoopQ", "Loop Questions i = 0 to Total-1", "rect", "#6366f1"),
            ("Match", "Compare Answer[i] == Key[i]?", "diamond", "#ec4899"),
            ("Score", "+4 Correct | -1 Incorrect | 0 Skipped", "rect", "#8b5cf6"),
            ("Net", "Net Score = (Correct*4) - (Incorrect*1)", "rect", "#10b981"),
            ("Sort", "Tie-Breaking Bubble Sort (Scores & Errors)", "rect", "#6366f1"),
            ("Stats", "Compute Item Difficulty & Success %", "rect", "#8b5cf6"),
            ("End", "Display Ranked Merit List -> End", "oval", "#3b82f6")
        ]
    },
    "Case_Study_42_Marks_Matrix_Analysis": {
        "title": "Case 42: Marks Matrix Analysis Flowchart",
        "nodes": [
            ("Start", "Start: Ingest Student Marks Matrix (N x K)", "oval", "#3b82f6"),
            ("RowLoop", "Row-Wise Loop: Iterate Students", "rect", "#6366f1"),
            ("StudentStats", "Calculate Total, Pct %, Grade & Pass/Fail", "rect", "#8b5cf6"),
            ("ColLoop", "Column-Wise Loop: Iterate Subjects", "rect", "#6366f1"),
            ("SubStats", "Calculate Subject Avg, Extremes, Pass %", "rect", "#8b5cf6"),
            ("CheckAlert", "Subject Avg < 60% OR Pass < 75%?", "diamond", "#ec4899"),
            ("Flag", "Flag Subject for Remedial Action", "rect", "#f59e0b"),
            ("Rank", "Bubble Sort: Rank Top Performers", "rect", "#10b981"),
            ("End", "Display Scorecard & Audit Report -> End", "oval", "#3b82f6")
        ]
    },
    "Case_Study_48_Shift_Conflict_Detector": {
        "title": "Case 48: Shift Conflict Detector Flowchart",
        "nodes": [
            ("Start", "Start: Load Immutable Shift Tuples", "oval", "#3b82f6"),
            ("Parse", "Convert HH:MM to Minutes from Midnight", "rect", "#6366f1"),
            ("DurCheck", "Duration <= 0 OR > 10 Hours?", "diamond", "#ec4899"),
            ("PairLoop", "Nested Loop: Compare Shift Pairs (i, j)", "rect", "#6366f1"),
            ("SameEmp", "Same Employee and Same Day?", "diamond", "#ec4899"),
            ("Overlap", "max(Start1, Start2) < min(End1, End2)?", "diamond", "#ec4899"),
            ("Rest", "Rest Interval < 8 Hours (480 mins)?", "diamond", "#ec4899"),
            ("LogViol", "Log Overlap / Rest / Duration Violations", "rect", "#ef4444"),
            ("End", "Display Shift Roster & Conflict Log -> End", "oval", "#3b82f6")
        ]
    },
    "Case_Study_56_Score_Balancing_Groups": {
        "title": "Case 56: Score Balancing Groups Flowchart",
        "nodes": [
            ("Start", "Start: Ingest Student Scores & K Teams", "oval", "#3b82f6"),
            ("Sort", "Bubble Sort Students Descending by Score", "rect", "#6366f1"),
            ("InitK", "Initialize K Empty Team Lists", "rect", "#8b5cf6"),
            ("Serpentine", "Serpentine Loop: Assign Forward 0..K-1", "rect", "#6366f1"),
            ("Reverse", "Reverse Direction: Assign Backward K-1..0", "rect", "#6366f1"),
            ("Metrics", "Compute Team Total, Mean, Min, Max", "rect", "#8b5cf6"),
            ("Disparity", "Calculate Disparity = Max Total - Min Total", "rect", "#10b981"),
            ("End", "Display Team Rosters & Balance Report -> End", "oval", "#3b82f6")
        ]
    },
    "Case_Study_75_Record_Consistency_Checker": {
        "title": "Case 75: Record Consistency Checker Flowchart",
        "nodes": [
            ("Start", "Start: Ingest Composite Student Tuples", "oval", "#3b82f6"),
            ("LoopRec", "Loop Through Records in Database", "rect", "#6366f1"),
            ("RollCheck", "Validate 8-Char Alphanumeric Syntax & Dupes", "diamond", "#ec4899"),
            ("NameCheck", "Validate Alphabetic Name & Length >= 2", "diamond", "#ec4899"),
            ("MarksCheck", "Validate Marks in [0.0, 100.0]", "diamond", "#ec4899"),
            ("AttCheck", "Validate Attendance in [0.0, 100.0]%", "diamond", "#ec4899"),
            ("HonorsCheck", "Honors Standing vs Marks/Attendance Check", "diamond", "#ec4899"),
            ("Catalog", "Separate Clean Records vs Defect Logs", "rect", "#10b981"),
            ("End", "Display Verified Table & Defect Audit -> End", "oval", "#3b82f6")
        ]
    },
    "Case_Study_91_Registration_Analyzer": {
        "title": "Case 91: Registration Analyzer Flowchart",
        "nodes": [
            ("Start", "Start: Ingest Raw Delimited Strings", "oval", "#3b82f6"),
            ("Delim", "Split by Pipe '|': Exactly 5 Fields?", "diamond", "#ec4899"),
            ("RegToken", "Validate REG#YYYY-DEPT-XXXX Syntax", "diamond", "#ec4899"),
            ("NameToken", "Extract & Sanitize NAME: (Underscores to Spaces)", "rect", "#8b5cf6"),
            ("DOBToken", "Validate DOB: YYYY-MM-DD Bounds", "diamond", "#ec4899"),
            ("EnumToken", "Validate Category & Status Allowed Values", "diamond", "#ec4899"),
            ("DupToken", "Check Duplicate Registration IDs", "diamond", "#ec4899"),
            ("TuplePack", "Pack Valid Structured 8-Element Tuple", "rect", "#10b981"),
            ("End", "Display Parsed Database & Error Log -> End", "oval", "#3b82f6")
        ]
    },
    "Case_Study_100_Campus_Management_Simulation": {
        "title": "Case 100: Smart Campus Simulation Flowchart",
        "nodes": [
            ("Start", "Start: Initialize Campus Multi-Entity State", "oval", "#3b82f6"),
            ("Acad", "Process Academics, Grades & 75% Attendance", "rect", "#6366f1"),
            ("Admit", "Barred Admit Cards for Deficient Students", "rect", "#f59e0b"),
            ("Events", "Process Event Registrations with Cap Limits", "diamond", "#ec4899"),
            ("Venues", "Schedule Labs/Venues with Collision Detection", "diamond", "#ec4899"),
            ("Analytics", "Generate University Executive Dashboard", "rect", "#10b981"),
            ("End", "Display Timetables & Rosters -> End", "oval", "#3b82f6")
        ]
    }
}

def generate_svg(title, nodes):
    width = 750
    node_height = 42
    node_width = 380
    gap = 26
    start_y = 65
    
    total_height = start_y + len(nodes) * (node_height + gap) + 40
    
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_height}" width="100%" height="{total_height}" style="background-color: #0f172a; font-family: Segoe UI, Roboto, Helvetica, Arial, sans-serif;">',
        '<defs>',
        '  <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">',
        '    <stop offset="0%" style="stop-color:#38bdf8;stop-opacity:1" />',
        '    <stop offset="100%" style="stop-color:#818cf8;stop-opacity:1" />',
        '  </linearGradient>',
        '  <filter id="shadow" x="-5%" y="-5%" width="115%" height="120%">',
        '    <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#000" flood-opacity="0.45" />',
        '  </filter>',
        '  <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
        '    <path d="M 0 1 L 8 5 L 0 9 z" fill="#38bdf8" />',
        '  </marker>',
        '</defs>',
        f'<text x="{width/2}" y="36" fill="#f8fafc" font-size="16" font-weight="bold" text-anchor="middle">{title}</text>'
    ]
    
    cx = width / 2
    for i, (node_id, text, shape, color) in enumerate(nodes):
        cy = start_y + i * (node_height + gap)
        nx = cx - (node_width / 2)
        ny = cy - (node_height / 2)
        
        # Connect to next node with arrow
        if i < len(nodes) - 1:
            next_cy = start_y + (i + 1) * (node_height + gap) - (node_height / 2)
            svg.append(f'  <line x1="{cx}" y1="{cy + node_height/2}" x2="{cx}" y2="{next_cy}" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#arrow)" />')
            
        # Draw node
        rx = 22 if shape == "oval" else (8 if shape == "diamond" else 6)
        stroke_color = "#38bdf8" if shape == "diamond" else "#94a3b8"
        svg.append(f'  <g filter="url(#shadow)">')
        svg.append(f'    <rect x="{nx}" y="{ny}" width="{node_width}" height="{node_height}" rx="{rx}" fill="{color}" stroke="{stroke_color}" stroke-width="1.8" />')
        svg.append(f'    <text x="{cx}" y="{cy + 5}" fill="#ffffff" font-size="13" font-weight="600" text-anchor="middle">{text}</text>')
        svg.append(f'  </g>')
        
    svg.append('</svg>')
    return '\n'.join(svg)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for folder, data in FLOWCHARTS.items():
        svg_content = generate_svg(data["title"], data["nodes"])
        target_path = os.path.join(base_dir, folder, "flowchart.svg")
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Generated {target_path}")

if __name__ == "__main__":
    main()
