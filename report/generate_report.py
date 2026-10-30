"""
Consolidated Academic Report Generator for Python Activity-Based Learning
Converts all 10 case study documentations, source codes, flowcharts, and execution logs
into a single, publication-quality HTML document and compiles it to PDF via Microsoft Edge.
"""

import os
import subprocess
import sys

CASE_DIRS = [
    ("Case 02: Progressive Electricity Billing and Anomaly Detection", "Case_Study_02_Electricity_Billing"),
    ("Case 26: Nested Loop Examination Seating Generator", "Case_Study_26_Seating_Arrangement"),
    ("Case 27: Advanced Numeric & Hollow Diamond Pattern Generator", "Case_Study_27_Pattern_Generator"),
    ("Case 31: String-Based Examination Answer Evaluation", "Case_Study_31_Answer_Key_Evaluator"),
    ("Case 42: Student Marks Matrix Analysis", "Case_Study_42_Marks_Matrix_Analysis"),
    ("Case 48: Tuple-Based Employee Shift Conflict Detection", "Case_Study_48_Shift_Conflict_Detector"),
    ("Case 56: Student Group Formation with Score Balancing", "Case_Study_56_Score_Balancing_Groups"),
    ("Case 75: Integrated Student Record Consistency Checker", "Case_Study_75_Record_Consistency_Checker"),
    ("Case 91: Advanced String-Based Registration Record Analyzer", "Case_Study_91_Registration_Analyzer"),
    ("Case 100: Comprehensive Smart Campus Management Simulation", "Case_Study_100_Campus_Management_Simulation")
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Python Activity-Based Learning Consolidated Report</title>
<style>
  @page {
    size: A4;
    margin: 18mm 15mm 18mm 15mm;
  }
  body {
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #1e293b;
    line-height: 1.55;
    background: #ffffff;
    font-size: 11pt;
    margin: 0;
    padding: 0;
  }
  .page-break {
    page-break-before: always;
  }
  .avoid-break {
    page-break-inside: avoid;
  }
  
  /* Cover Page Styling */
  .cover {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    border: 3px double #1e3a8a;
    padding: 40px 25px;
    box-sizing: border-box;
  }
  .inst-header {
    font-size: 22pt;
    font-weight: 800;
    color: #1e3a8a;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 4px;
  }
  .inst-sub {
    font-size: 11pt;
    color: #475569;
    margin-bottom: 25px;
  }
  .report-title {
    font-size: 20pt;
    font-weight: 700;
    color: #0f172a;
    background: #f1f5f9;
    padding: 18px 24px;
    border-radius: 8px;
    border-left: 6px solid #2563eb;
    margin: 30px 0;
    width: 88%;
  }
  .report-sub {
    font-size: 13pt;
    color: #2563eb;
    font-weight: 600;
  }
  .meta-box {
    margin-top: 40px;
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 22px 30px;
    text-align: left;
    width: 75%;
    font-size: 11.5pt;
  }
  .meta-box table {
    width: 100%;
    border-collapse: collapse;
  }
  .meta-box td {
    padding: 6px 10px;
  }
  .meta-box td.label {
    font-weight: 700;
    color: #334155;
    width: 35%;
  }

  /* Document Content Styling */
  h1.case-title {
    color: #1e3a8a;
    font-size: 17pt;
    border-bottom: 2px solid #2563eb;
    padding-bottom: 6px;
    margin-top: 15px;
    margin-bottom: 15px;
  }
  h2.section-header {
    color: #0f172a;
    font-size: 12.5pt;
    margin-top: 18px;
    margin-bottom: 8px;
    border-left: 4px solid #3b82f6;
    padding-left: 8px;
  }
  p, li {
    font-size: 10.5pt;
    color: #334155;
    margin: 4px 0;
  }
  ul, ol {
    margin-top: 4px;
    margin-bottom: 8px;
    padding-left: 22px;
  }
  
  /* Tables */
  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 9.5pt;
  }
  table.data-table th, table.data-table td {
    border: 1px solid #cbd5e1;
    padding: 6px 9px;
    text-align: left;
  }
  table.data-table th {
    background-color: #f1f5f9;
    color: #1e293b;
    font-weight: 700;
  }
  table.data-table tr:nth-child(even) {
    background-color: #f8fafc;
  }

  /* Code & Pre */
  pre.code-block {
    background: #0f172a;
    color: #e2e8f0;
    padding: 12px;
    border-radius: 6px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
    line-height: 1.4;
    overflow-x: auto;
    border: 1px solid #334155;
    margin: 8px 0;
  }
  pre.output-block {
    background: #1e1e1e;
    color: #4ade80;
    padding: 12px;
    border-radius: 6px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
    line-height: 1.35;
    white-space: pre-wrap;
    border: 1px solid #374151;
    margin: 8px 0;
  }

  .diagram-container {
    text-align: center;
    margin: 15px 0;
    background: #0f172a;
    padding: 15px;
    border-radius: 8px;
    page-break-inside: avoid;
  }
  .badge {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 8.5pt;
    font-weight: bold;
    background: #dbeafe;
    color: #1e40af;
  }
</style>
</head>
<body>

<!-- Cover Page -->
<div class="cover">
  <div class="inst-header">Dr. RVR NRI Institute of Technology</div>
  <div class="inst-sub">An Institution Deemed to be University u/s 3 of UGC Act, 1956<br>Pothavarappadu (V), Agiripalli (M), Vijayawada Rural, Eluru Dist., Andhra Pradesh</div>
  
  <div style="font-size: 14pt; font-weight: bold; color: #475569; text-transform: uppercase; letter-spacing: 1px;">
    School of Computer Studies
  </div>
  
  <div class="report-title">
    <div class="report-sub">I B.Tech. - Python Programming Course</div>
    Activity-Based Learning (ABL) Assignment
    <div style="font-size: 11pt; font-weight: normal; color: #475569; margin-top: 8px;">
      Comprehensive Technical Report on 10 Selected Difficult-Level Case Studies
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
      <tr>
        <td class="label">Academic Program:</td>
        <td>B.Tech. in Computer Science & Engineering</td>
      </tr>
      <tr>
        <td class="label">Section / Year:</td>
        <td>Section A | I Year (2026–2027)</td>
      </tr>
      <tr>
        <td class="label">Faculty Mentor:</td>
        <td>Department of Computer Science & Engineering</td>
      </tr>
      <tr>
        <td class="label">GitHub Repository:</td>
        <td><code>Python-Activity-Based-Learning</code></td>
      </tr>
      <tr>
        <td class="label">Date of Submission:</td>
        <td>October 2026</td>
      </tr>
    </table>
  </div>
</div>

<div class="page-break"></div>

<!-- Table of Contents & Executive Summary -->
<h1 class="case-title" style="text-align: center;">Executive Summary & Syllabus Mapping</h1>
<p>
This consolidated laboratory report fulfills the requirements of the <strong>Python Programming Activity-Based Learning (ABL) Assignment</strong> issued by the Dean of Computer Studies and Course Coordinator at Dr. RVR NRI Institute of Technology. Ten high-rigor, difficult-level case studies were engineered covering the entire breadth of the foundational syllabus without introducing prohibited external libraries.
</p>

<h2 class="section-header">Summary of Selected Case Studies</h2>
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
