"""Check student records for common mistakes."""

def validate_roll_number_format(roll_no):
    """
    Validates institutional roll number syntax: e.g., '26CSE101'
    Format: 2 digits (Year) + 3 letters (Branch: CSE/ECE/MEC/INF) + 3 digits (Serial)
    Length must be exactly 8 characters.
    """
    if not isinstance(roll_no, str):
        return False, "Roll number must be a string."
    if len(roll_no) != 8:
        return False, f"Invalid length {len(roll_no)}; roll number must be exactly 8 characters."
        
    year_part = roll_no[:2]
    branch_part = roll_no[2:5].upper()
    serial_part = roll_no[5:]
    
    if not (year_part.isdigit() and serial_part.isdigit()):
        return False, "Year prefix (first 2) and serial (last 3) must be numeric digits."
        
    valid_branches = ["CSE", "ECE", "MEC", "INF", "CIV", "EEE"]
    if branch_part not in valid_branches:
        return False, f"Unknown department code '{branch_part}'. Must be one of {valid_branches}."
        
    return True, "Valid"


def validate_student_name(name):
    """Validates student full name: must have at least 2 alphabetic characters."""
    if not isinstance(name, str):
        return False, "Name must be a string."
    cleaned = name.replace(" ", "").replace(".", "")
    if len(cleaned) < 2:
        return False, "Name is too short (less than 2 characters)."
    if not cleaned.isalpha():
        return False, f"Name contains invalid non-alphabetic characters: '{name}'."
    return True, "Valid"


def validate_marks_tuple(marks):
    """Validates tuple of marks: must be non-empty, all numbers within [0.0, 100.0]."""
    if not isinstance(marks, tuple):
        return False, "Marks record must be structured as a tuple."
    if len(marks) == 0:
        return False, "Marks tuple is empty."
    for m in marks:
        if not (isinstance(m, int) or isinstance(m, float)):
            return False, f"Non-numeric mark encountered: {m}"
        if m < 0.0 or m > 100.0:
            return False, f"Mark {m} out of valid bounds [0.0, 100.0]."
    return True, "Valid"


def validate_attendance(att_pct):
    """Validates attendance percentage: must be between 0.0 and 100.0."""
    if not (isinstance(att_pct, int) or isinstance(att_pct, float)):
        return False, "Attendance must be a numeric percentage."
    if att_pct < 0.0 or att_pct > 100.0:
        return False, f"Attendance {att_pct}% out of range [0.0, 100.0]."
    return True, "Valid"


def audit_student_database(records):
    """
    Audits a database list of student tuples:
    (roll_no, name, marks_tuple, attendance_pct, fee_paid, standing)
    Detects duplicate IDs, format errors, value anomalies, and academic contradictions.
    """
    seen_roll_numbers = []
    clean_records = []
    defect_log = []
    
    for idx in range(len(records)):
        entry = records[idx]
        record_num = idx + 1
        
        # Verify tuple structure
        if not isinstance(entry, tuple) or len(entry) != 6:
            defect_log.append((record_num, "MALFORMED_RECORD", "Record is not a 6-element tuple.", str(entry)))
            continue
            
        roll_no, name, marks, att, fee, standing = entry
        entry_defects = []
        
        # 1. Roll number format
        is_roll_ok, roll_msg = validate_roll_number_format(roll_no)
        if not is_roll_ok:
            entry_defects.append(f"Roll Error: {roll_msg}")
        else:
            # Check duplicates
            if roll_no in seen_roll_numbers:
                entry_defects.append(f"DUPLICATE_ID: Roll number '{roll_no}' has already been registered.")
            else:
                seen_roll_numbers.append(roll_no)
                
        # 2. Name validation
        is_name_ok, name_msg = validate_student_name(name)
        if not is_name_ok:
            entry_defects.append(f"Name Error: {name_msg}")
            
        # 3. Marks validation
        is_marks_ok, marks_msg = validate_marks_tuple(marks)
        if not is_marks_ok:
            entry_defects.append(f"Marks Error: {marks_msg}")
            
        # 4. Attendance validation
        is_att_ok, att_msg = validate_attendance(att)
        if not is_att_ok:
            entry_defects.append(f"Attendance Error: {att_msg}")
            
        # 5. Fee status validation
        if not isinstance(fee, bool):
            entry_defects.append(f"Fee status must be a boolean True/False (got {fee}).")
            
        # 6. Academic Standing Contradiction Check
        # If standing == "HONORS", student must have att >= 75%, fee == True, and all marks >= 60.0
        if standing == "HONORS":
            if is_marks_ok:
                min_m = marks[0]
                for m in marks:
                    if m < min_m:
                        min_m = m
                if min_m < 60.0:
                    entry_defects.append(f"Contradiction: Student marked 'HONORS' but has a low mark ({min_m} < 60.0).")
            if is_att_ok and att < 75.0:
                entry_defects.append(f"Contradiction: Student marked 'HONORS' but attendance is deficient ({att}% < 75%).")
                
        # Catalog verdict
        if len(entry_defects) > 0:
            defect_log.append((record_num, "INTEGRITY_VIOLATION", "; ".join(entry_defects), roll_no))
        else:
            clean_records.append(entry)
            
    return clean_records, defect_log


def display_audit_report(total_scanned, clean_records, defect_log):
    """Renders formatted student database consistency report."""
    border = "=" * 94
    dash = "-" * 94
    
    print("\n" + border)
    print(" " * 22 + "DR. RVR NRI INSTITUTE OF TECHNOLOGY")
    print(" " * 20 + "ACADEMIC DATABASE CONSISTENCY & INTEGRITY AUDIT")
    print(border)
    print(f"Total Raw Records Ingested : {total_scanned}")
    print(f"Verified Consistent Records: {len(clean_records)} ({round(len(clean_records)/total_scanned*100, 1)}%)")
    print(f"Defective / Flagged Records: {len(defect_log)} ({round(len(defect_log)/total_scanned*100, 1)}%)")
    print(dash)
    
    print("VERIFIED CLEAN STUDENT RECORDS:")
    print(f"{'Roll No':<11}{'Student Name':<20}{'Marks':<22}{'Att %':>8}{'Fee':>7}{'Standing':>12}")
    print(dash)
    for rec in clean_records:
        r, n, m, a, f, s = rec
        marks_str = str(m)
        fee_str = "PAID" if f else "DUE"
        print(f"{r:<11}{n:<20}{marks_str:<22}{a:>7.1f}%{fee_str:>7}  {s:>12}")
        
    print(dash)
    
    if len(defect_log) > 0:
        print("[!] INTEGRITY DEFECT & INCONSISTENCY LOG:")
        for defect in defect_log:
            rec_id, cat, desc, ref = defect
            print(f"    - Record #{rec_id} (Ref: {ref}) | Type: {cat}")
            print(f"      Defects: {desc}")
    else:
        print("[*] Academic database contains zero defects or inconsistencies.")
        
    print(border + "\n")


def run_demo():
    """Demo database containing clean records, duplicates, bad formats, and contradictions."""
    sample_database = [
        # 1. Clean valid record
        ("26CSE101", "Aaditya Roy", (92.0, 88.0, 95.0), 86.5, True, "HONORS"),
        
        # 2. Duplicate Roll Number (26CSE101 repeated)
        ("26CSE101", "Bhavya Sri", (80.0, 75.0, 82.0), 90.0, True, "REGULAR"),
        
        # 3. Invalid Roll format (year non-digit, dept code invalid 'XYZ')
        ("XXXYZ999", "Charan Teja", (65.0, 70.0, 68.0), 78.0, True, "REGULAR"),
        
        # 4. Out-of-bounds mark (-15.0 and 110.0)
        ("26ECE201", "Divya Reddy", (-15.0, 85.0, 110.0), 82.0, True, "REGULAR"),
        
        # 5. Invalid attendance (> 100%) and short/numeric name
        ("26MEC301", "E1", (60.0, 65.0, 70.0), 108.5, False, "PROBATION"),
        
        # 6. Academic Contradiction: Marked HONORS but attendance is only 62.0% (< 75%)
        ("26INF401", "Farhan Akhtar", (88.0, 92.0, 90.0), 62.0, True, "HONORS"),
        
        # 7. Another clean valid record
        ("26CSE102", "Gautam Krishna", (78.0, 82.0, 79.0), 84.0, True, "REGULAR")
    ]
    
    clean, defects = audit_student_database(sample_database)
    display_audit_report(len(sample_database), clean, defects)


if __name__ == "__main__":
    run_demo()
