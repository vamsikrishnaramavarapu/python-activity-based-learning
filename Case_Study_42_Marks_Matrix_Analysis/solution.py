"""Calculate student grades and check subject results."""

def compute_grade(percentage, has_failed_any_subject):
    """Determine letter grade according to academic grading scale."""
    if has_failed_any_subject or percentage < 40.0:
        return "F"
    elif percentage >= 90.0:
        return "O"
    elif percentage >= 80.0:
        return "A+"
    elif percentage >= 70.0:
        return "A"
    elif percentage >= 60.0:
        return "B+"
    elif percentage >= 50.0:
        return "B"
    else:
        return "C"


def analyze_student_matrix(students_info, subjects, marks_matrix):
    """
    Analyzes 2D marks matrix (nested lists).
    students_info: list of tuples (roll_no, student_name)
    subjects: list of subject names (e.g., ['Math', 'Physics', 'Python', 'Electronics'])
    marks_matrix: nested list where marks_matrix[i][j] is mark of student i in subject j
    """
    num_students = len(students_info)
    num_subjects = len(subjects)
    pass_mark_per_subject = 40.0
    
    # 1. Row-Wise Analysis (Student Performance)
    student_summaries = []
    
    for i in range(num_students):
        roll_no, name = students_info[i]
        marks_row = marks_matrix[i]
        
        row_total = 0
        failed_count = 0
        min_mark = 101.0
        max_mark = -1.0
        
        for mark in marks_row:
            row_total += mark
            if mark < pass_mark_per_subject:
                failed_count += 1
            if mark < min_mark:
                min_mark = mark
            if mark > max_mark:
                max_mark = mark
                
        percentage = round((row_total / (num_subjects * 100)) * 100, 2)
        has_failed = failed_count > 0
        grade = compute_grade(percentage, has_failed)
        status = "PASSED" if not has_failed else f"FAILED ({failed_count} Sub)"
        
        student_summaries.append((
            roll_no,
            name,
            marks_row,
            row_total,
            percentage,
            grade,
            status
        ))
        
    # 2. Column-Wise Analysis (Subject Performance)
    subject_summaries = []
    
    for j in range(num_subjects):
        col_total = 0
        col_max = -1.0
        col_min = 101.0
        pass_count = 0
        
        for i in range(num_students):
            m = marks_matrix[i][j]
            col_total += m
            if m >= pass_mark_per_subject:
                pass_count += 1
            if m > col_max:
                col_max = m
            if m < col_min:
                col_min = m
                
        sub_avg = round(col_total / num_students, 2) if num_students > 0 else 0.0
        sub_pass_pct = round((pass_count / num_students) * 100, 2) if num_students > 0 else 0.0
        needs_attention = (sub_avg < 60.0) or (sub_pass_pct < 75.0)
        
        subject_summaries.append((
            subjects[j],
            sub_avg,
            col_max,
            col_min,
            sub_pass_pct,
            needs_attention
        ))
        
    return student_summaries, subject_summaries


def rank_students(student_summaries):
    """Rank students based on total marks using bubble sort."""
    ranked = []
    for item in student_summaries:
        ranked.append(item)
        
    n = len(ranked)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if ranked[j][3] < ranked[j + 1][3]:  # Compare total marks
                temp = ranked[j]
                ranked[j] = ranked[j + 1]
                ranked[j + 1] = temp
                
    return ranked


def display_matrix_report(subjects, student_summaries, subject_summaries):
    """Render a comprehensive academic scorecard and diagnostic report."""
    border = "=" * 98
    dash = "-" * 98
    
    print("\n" + border)
    print(" " * 26 + "DR. RVR NRI INSTITUTE OF TECHNOLOGY")
    print(" " * 24 + "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING")
    print(" " * 23 + "SEMESTER MARKS MATRIX & PERFORMANCE AUDIT")
    print(border)
    
    # Table Header with Dynamic Subject Columns
    header = f"{'Roll No':<10}{'Student Name':<16}"
    for sub in subjects:
        header += f"{sub[:6]:>8}"
    header += f"{'Total':>9}{'Pct %':>8}{'Grade':>7}{'Status':>16}"
    print(header)
    print(dash)
    
    # Print Student Rows
    for s in student_summaries:
        roll, name, marks, total, pct, grade, status = s
        row_str = f"{roll:<10}{name:<16}"
        for m in marks:
            row_str += f"{m:>8.1f}"
        row_str += f"{total:>9.1f}{pct:>7.1f}%{grade:>6}  {status:<16}"
        print(row_str)
        
    print(dash)
    
    # Column-Wise Summary Footer
    avg_row = f"{'SUBJECT AVG':<26}"
    for sub_stat in subject_summaries:
        s_name, s_avg, _, _, _, _ = sub_stat
        avg_row += f"{s_avg:>8.1f}"
    print(avg_row)
    
    pass_pct_row = f"{'SUBJECT PASS %':<26}"
    for sub_stat in subject_summaries:
        _, _, _, _, s_pass, _ = sub_stat
        pass_pct_row += f"{s_pass:>7.1f}%"
    print(pass_pct_row)
    print(dash)
    
    # Top Performers (Merit List)
    ranked = rank_students(student_summaries)
    print("\n[*] TOP ACADEMIC PERFORMERS (MERIT RANKING):")
    top_limit = 3 if len(ranked) >= 3 else len(ranked)
    for r in range(top_limit):
        roll, name, _, tot, pct, gr, _ = ranked[r]
        print(f"    Rank #{r + 1}: {name} ({roll}) | Total: {tot:.1f} / {len(subjects)*100} ({pct}%) | Grade: {gr}")
        
    print("\n[!] CURRICULUM INTERVENTION ALERTS (LOW-PERFORMING SUBJECTS):")
    flagged = False
    for sub_stat in subject_summaries:
        s_name, s_avg, s_max, s_min, s_pass, needs_att = sub_stat
        if needs_att:
            flagged = True
            print(f"    - Subject: {s_name} | Class Average: {s_avg:.1f} | Pass Rate: {s_pass:.1f}%")
            print(f"      Root Cause: Class average below 60.0% or pass rate below 75.0%. Remedial sessions recommended.")
    if not flagged:
        print("    All subjects met institutional performance thresholds.")
    print(border + "\n")


def run_demo():
    """Run demonstration with 6 students across 5 subjects."""
    subjects = ["Maths", "Physics", "Python", "DataStr", "Digital"]
    
    students_info = [
        ("26CSE01", "Aaditya Roy"),
        ("26CSE02", "Bhavya Sri"),
        ("26CSE03", "Charan Teja"),
        ("26CSE04", "Divya Reddy"),
        ("26CSE05", "Eshwar Rao"),
        ("26CSE06", "Fatima Zahra")
    ]
    
    # 6 x 5 Nested List Marks Matrix
    marks_matrix = [
        [94.0, 88.0, 96.0, 91.0, 89.0],  # Top student
        [78.0, 72.0, 85.0, 68.0, 74.0],  # Strong student
        [32.0, 54.0, 62.0, 38.0, 50.0],  # Failed in Maths (32) and DataStr (38)
        [88.0, 82.0, 90.0, 84.0, 86.0],  # High performer
        [45.0, 48.0, 55.0, 42.0, 51.0],  # Just passed all
        [65.0, 58.0, 72.0, 35.0, 60.0]   # Failed in DataStr (35)
    ]
    
    student_summaries, subject_summaries = analyze_student_matrix(students_info, subjects, marks_matrix)
    display_matrix_report(subjects, student_summaries, subject_summaries)


if __name__ == "__main__":
    run_demo()
