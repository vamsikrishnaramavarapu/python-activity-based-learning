"""Build a simple HTML and PDF report from the case study files."""

import os
import subprocess
import sys

CASE_DIRS = [
    ("Case 02: Electricity Bill", "Case_Study_02_Electricity_Billing"),
    ("Case 26: Exam Seating Plan", "Case_Study_26_Seating_Arrangement"),
    ("Case 27: Number Patterns", "Case_Study_27_Pattern_Generator"),
    ("Case 31: Answer Key", "Case_Study_31_Answer_Key_Evaluator"),
    ("Case 42: Marks Analysis", "Case_Study_42_Marks_Matrix_Analysis"),
    ("Case 48: Shift Checker", "Case_Study_48_Shift_Conflict_Detector"),
    ("Case 56: Student Groups", "Case_Study_56_Score_Balancing_Groups"),
    ("Case 75: Student Record Checker", "Case_Study_75_Record_Consistency_Checker"),
    ("Case 91: Registration Checker", "Case_Study_91_Registration_Analyzer"),
    ("Case 100: Campus Management", "Case_Study_100_Campus_Management_Simulation")
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Python Activity-Based Learning Consolidated Report</title>
<style>
  @page { size: A4; margin: 18mm; }
  body {
    font-family: Arial, sans-serif;
    color: #222;
    line-height: 1.5;
    font-size: 11pt;
    margin: 0;
  }
  .page-break { page-break-before: always; }
  .cover {
    min-height: 90vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    border: 2px solid #444;
    padding: 24px;
    box-sizing: border-box;
  }
  .inst-header { font-size: 20pt; font-weight: bold; }
  .inst-sub { margin-top: 8px; }
  .report-title {
    font-size: 18pt;
    margin: 28px 0;
    padding: 16px;
    border: 1px solid #777;
    width: 85%;
  }
  .report-sub { font-size: 13pt; margin-bottom: 8px; }
  .meta-box { margin-top: 18px; text-align: left; }
  .meta-box table { border-collapse: collapse; }
  .meta-box td { padding: 5px 10px; }
  .meta-box td.label { font-weight: bold; }
  h1.case-title {
    font-size: 17pt;
    border-bottom: 1px solid #555;
    padding-bottom: 6px;
  }
  h2.section-header { font-size: 13pt; margin-top: 18px; }
  p, li { font-size: 10.5pt; }
  table.data-table { width: 100%; border-collapse: collapse; margin: 12px 0; }
  table.data-table th, table.data-table td {
    border: 1px solid #888;
    padding: 5px;
    text-align: left;
  }
  table.data-table th { background: #eee; }
  pre.code-block, pre.output-block {
    background: #f5f5f5;
    color: #222;
    padding: 10px;
    font-family: Consolas, monospace;
    font-size: 8.5pt;
    line-height: 1.35;
    white-space: pre-wrap;
    border: 1px solid #aaa;
  }
  .diagram-container { text-align: center; margin: 12px 0; }
</style>
</head>
<body>

<!-- Cover Page -->
<div class="cover">
  <div class="inst-header">Python Programming</div>
  <div class="inst-sub">I B.Tech. | Activity-Based Learning Assignment</div>
  
  <div class="report-title">
    <div class="report-sub">10 Case Studies</div>
    Activity-Based Learning
    <div style="font-size: 11pt; font-weight: normal; margin-top: 8px;">
      Programs, flowcharts, and example output
    </div>
  </div>

  <div class="meta-box">
    <table>
      <tr>
        <td class="label">Student Name:</td>
        <td><strong>[YOUR NAME HERE]</strong></td>
      </tr>
      <tr>
        <td class="label">Roll Number:</td>
        <td><strong>[YOUR ROLL NUMBER HERE]</strong></td>
      </tr>
      <tr><td class="label">Branch:</td><td>Computer Science & Engineering</td></tr>
      <tr><td class="label">Year:</td><td>I B.Tech.</td></tr>
    </table>
  </div>
</div>

<div class="page-break"></div>

<!-- Table of Contents & Executive Summary -->
<h1 class="case-title" style="text-align: center;">About this project</h1>
<p>
This report contains the 10 Python programs in this folder. They use sample data to show ideas like loops, conditions, strings, lists, and tuples. Each case has a short explanation, a flowchart, the code, and its example output.
</p>

<h2 class="section-header">Case studies</h2>
<table class="data-table">
  <thead>
    <tr>
      <th style="width: 8%;">Case #</th>
      <th style="width: 42%;">Title</th>
      <th style="width: 50%;">Syllabus Concepts Demonstrated</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Case 02</strong></td>
      <td>Progressive Electricity Billing and Anomaly Detection</td>
      <td>Progressive Tariff Slabs, Fixed Fees, Surcharges, Rebates, Lists, Multi-Month Comparison</td>
    </tr>
    <tr>
      <td><strong>Case 26</strong></td>
      <td>Nested Loop Examination Seating Generator</td>
      <td>2D Nested Lists, Coordinate Offsets, Adjacency Conflict Prevention, Reserved Desks</td>
    </tr>
    <tr>
      <td><strong>Case 27</strong></td>
      <td>Advanced Numeric & Hollow Diamond Pattern Generator</td>
      <td>Parity Validation, Nested Loops, Geometric Symmetry, Palindromic Multi-tier Numbers</td>
    </tr>
    <tr>
      <td><strong>Case 31</strong></td>
      <td>String-Based Examination Answer Evaluation</td>
      <td>String Traversal, Slicing, Negative Marking, Bubble Sort Tie-Breaking, Item Analytics</td>
    </tr>
    <tr>
      <td><strong>Case 42</strong></td>
      <td>Student Marks Matrix Analysis & Performance Classification</td>
      <td>2D Nested Lists, Dual-Axis Matrix Reductions, Grade Assignments, Remedial Intervention Alerts</td>
    </tr>
    <tr>
      <td><strong>Case 48</strong></td>
      <td>Tuple-Based Employee Shift Conflict Detection</td>
      <td>Immutable Tuples, Time Parsing (HH:MM to Mins), Interval Collision Logic, Rest Auditing</td>
    </tr>
    <tr>
      <td><strong>Case 56</strong></td>
      <td>Student Group Formation with Score Balancing</td>
      <td>Serpentine (Snake Draft) Allocation Algorithm, Score Variance Minimization, Nested Rosters</td>
    </tr>
    <tr>
      <td><strong>Case 75</strong></td>
      <td>Integrated Student Record Consistency Checker</td>
      <td>Alphanumeric Syntax Validation, Duplicate ID Detection, Mark/Attendance Ranges, Contradiction Trapping</td>
    </tr>
    <tr>
      <td><strong>Case 91</strong></td>
      <td>Advanced String-Based Registration Record Analyzer</td>
      <td>Delimited Tokenization, Format Grammar, Calendar Validation, Categorized Defect Audit</td>
    </tr>
    <tr>
      <td><strong>Case 100</strong></td>
      <td>Comprehensive Smart Campus Management Simulation</td>
      <td>Capstone Integration: Academics, 75% Attendance Gating, Event Caps, Venue Scheduling</td>
    </tr>
  </tbody>
</table>

<!-- Case Studies Injected Here -->
{CASE_STUDIES_CONTENT}

</body>
</html>
"""

def read_file_safe(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def markdown_to_html_simple(md_text):
    """Simple parser to convert markdown sections into clean HTML tags."""
    lines = md_text.splitlines()
    html_out = []
    in_code = False
    in_table = False
    table_header_done = False
    
    for line in lines:
        stripped = line.strip()
        
        # Skip top level title as we format it specially
        if stripped.startswith("# Case Study"):
            continue
            
        if stripped.startswith("```"):
            if in_code:
                html_out.append("</pre>")
                in_code = False
            else:
                lang = stripped[3:].strip()
                if "mermaid" in lang:
                    in_code = False
                    continue  # We embed visual SVG instead
                html_out.append("<pre class='code-block'>")
                in_code = True
            continue
            
        if in_code:
            html_out.append(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
            continue
            
        # Tables
        if "|" in stripped and ("---" in stripped or (stripped.startswith("|") and stripped.endswith("|"))):
            if "---" in stripped:
                continue
            cols = [c.strip() for c in stripped.split("|")[1:-1]]
            if not in_table:
                html_out.append("<table class='data-table'>")
                html_out.append("<thead><tr>" + "".join([f"<th>{c}</th>" for c in cols]) + "</tr></thead><tbody>")
                in_table = True
                continue
            else:
                html_out.append("<tr>" + "".join([f"<td>{c}</td>" for c in cols]) + "</tr>")
                continue
        elif in_table:
            html_out.append("</tbody></table>")
            in_table = False
            
        if stripped.startswith("## "):
            header_text = stripped[3:]
            html_out.append(f"<h2 class='section-header'>{header_text}</h2>")
        elif stripped.startswith("- "):
            html_out.append(f"<li>{stripped[2:]}</li>")
        elif stripped.startswith("1. ") or stripped.startswith("2. ") or stripped.startswith("3. ") or stripped.startswith("4. ") or stripped.startswith("5. "):
            html_out.append(f"<li>{stripped[3:]}</li>")
        elif len(stripped) > 0:
            html_out.append(f"<p>{stripped}</p>")
            
    if in_table:
        html_out.append("</tbody></table>")
    if in_code:
        html_out.append("</pre>")
        
    return "\n".join(html_out)


def build_consolidated_report():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_sections = []
    
    for case_title, folder in CASE_DIRS:
        case_path = os.path.join(base_dir, folder)
        readme_path = os.path.join(case_path, "README.md")
        code_path = os.path.join(case_path, "solution.py")
        svg_path = os.path.join(case_path, "flowchart.svg")
        out_path = os.path.join(case_path, "output.txt")
        
        md_content = read_file_safe(readme_path)
        code_content = read_file_safe(code_path)
        svg_content = read_file_safe(svg_path)
        out_content = read_file_safe(out_path)
        
        # Clean svg for embedding
        if "<svg" in svg_content:
            svg_inline = svg_content[svg_content.find("<svg"):]
        else:
            svg_inline = ""
            
        section_html = [
            '<div class="page-break"></div>',
            f'<h1 class="case-title">{case_title}</h1>',
            markdown_to_html_simple(md_content),
            '<h2 class="section-header">Visual Program Flowchart Diagram</h2>',
            f'<div class="diagram-container">{svg_inline}</div>',
            '<h2 class="section-header">Complete Python Source Code</h2>',
            f'<pre class="code-block">{code_content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</pre>',
            '<h2 class="section-header">Verified Console Output / Execution Capture</h2>',
            f'<pre class="output-block">{out_content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</pre>'
        ]
        
        report_sections.append("\n".join(section_html))
        
    full_html = HTML_TEMPLATE.replace("{CASE_STUDIES_CONTENT}", "\n".join(report_sections))
    
    out_html_path = os.path.join(base_dir, "report", "consolidated_report.html")
    os.makedirs(os.path.dirname(out_html_path), exist_ok=True)
    with open(out_html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    print(f"Generated HTML report: {out_html_path}")
    
    # Compile to PDF using Microsoft Edge Headless
    pdf_path = os.path.join(base_dir, "report", "Python_Activity_Based_Learning_Report.pdf")
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    edge_bin = None
    for p in edge_paths:
        if os.path.exists(p):
            edge_bin = p
            break
            
    if edge_bin:
        print(f"Rendering PDF via Headless Microsoft Edge ({edge_bin})...")
        cmd = [
            edge_bin,
            "--headless",
            "--disable-gpu",
            "--run-all-compositor-stages-before-draw",
            f"--print-to-pdf={pdf_path}",
            f"file:///{out_html_path.replace(os.sep, '/')}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(pdf_path):
            size_kb = os.path.getsize(pdf_path) / 1024
            print(f"[SUCCESS] PDF Generated Successfully: {pdf_path} ({size_kb:.1f} KB)")
        else:
            print("[WARNING] Edge completed, but PDF file was not detected.")
    else:
        print("[WARNING] Microsoft Edge executable not found. PDF must be printed manually from consolidated_report.html.")


if __name__ == "__main__":
    build_consolidated_report()
