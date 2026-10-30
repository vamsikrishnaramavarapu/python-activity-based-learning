"""
Case Study 48: Tuple-Based Employee Shift Conflict Detection
Syllabus Concepts: Computational Thinking, Variables, Operators, Conditional Statements,
                   Loops, Strings, Lists, Tuples, and Tuple Unpacking.
"""

def parse_time_to_minutes(time_str):
    """
    Converts 24-hour format string 'HH:MM' into integer minutes since midnight.
    Example: '09:30' -> 9 * 60 + 30 = 570
    """
    parts = time_str.strip().split(":")
    hours = int(parts[0])
    minutes = int(parts[1])
    return hours * 60 + minutes


def minutes_to_time_str(total_minutes):
    """Converts integer minutes since midnight back to 'HH:MM' string."""
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours:02d}:{minutes:02d}"


def detect_shift_conflicts(shift_tuples):
    """
    Analyzes list of shift tuples:
    (shift_id, emp_id, emp_name, day, start_str, end_str, dept)
    Detects:
    1. Direct Time Overlaps for the same employee on the same day.
    2. Insufficient Rest (< 480 mins / 8 hours) between shifts on the same day.
    3. Excessive Shift Duration (> 10 hours / 600 mins).
    """
    num_shifts = len(shift_tuples)
    conflicts = []
    
    # 1. Single Shift Duration Audit
    for shift in shift_tuples:
        s_id, e_id, name, day, s_str, e_str, dept = shift
        s_min = parse_time_to_minutes(s_str)
        e_min = parse_time_to_minutes(e_str)
        duration = e_min - s_min
        
        if duration <= 0:
            conflicts.append((
                "INVALID_TIMING",
                f"Shift {s_id} for {name} ({e_id}) on {day} has invalid duration (Ends at or before start: {s_str} - {e_str}).",
                (s_id,)
            ))
        elif duration > 600:  # > 10 hours
            conflicts.append((
                "EXCESSIVE_DURATION",
                f"Shift {s_id} for {name} ({e_id}) on {day} exceeds maximum daily work limit: {duration//60}h {duration%60}m > 10h limit.",
                (s_id,)
            ))
            
    # 2. Pairwise Shift Comparison using nested loops
    for i in range(num_shifts):
        s1 = shift_tuples[i]
        id1, emp1, name1, day1, start1_str, end1_str, dept1 = s1
        start1 = parse_time_to_minutes(start1_str)
        end1 = parse_time_to_minutes(end1_str)
        
        for j in range(i + 1, num_shifts):
            s2 = shift_tuples[j]
            id2, emp2, name2, day2, start2_str, end2_str, dept2 = s2
            start2 = parse_time_to_minutes(start2_str)
            end2 = parse_time_to_minutes(end2_str)
            
            # Conflicts occur if both shifts belong to the same employee on the same day
            if emp1 == emp2 and day1 == day2:
                # Check Overlap: max(start1, start2) < min(end1, end2)
                overlap_start = start1 if start1 > start2 else start2
                overlap_end = end1 if end1 < end2 else end2
                
                if overlap_start < overlap_end:
                    overlap_duration = overlap_end - overlap_start
                    conflicts.append((
                        "DIRECT_OVERLAP",
                        f"Collision between {id1} ({start1_str}-{end1_str}) and {id2} ({start2_str}-{end2_str}) for {name1} ({emp1}) on {day1}. Overlap: {overlap_duration} mins.",
                        (id1, id2)
                    ))
                else:
                    # Check Rest Interval between successive shifts
                    # Case A: Shift 1 ends before Shift 2 starts
                    if end1 <= start2:
                        rest_gap = start2 - end1
                        if rest_gap < 480:  # Less than 8 hours rest
                            conflicts.append((
                                "INSUFFICIENT_REST",
                                f"Rest violation between {id1} and {id2} for {name1} on {day1}: Rest gap is only {rest_gap//60}h {rest_gap%60}m (< 8h required).",
                                (id1, id2)
                            ))
                    # Case B: Shift 2 ends before Shift 1 starts
                    elif end2 <= start1:
                        rest_gap = start1 - end2
                        if rest_gap < 480:
                            conflicts.append((
                                "INSUFFICIENT_REST",
                                f"Rest violation between {id2} and {id1} for {name1} on {day1}: Rest gap is only {rest_gap//60}h {rest_gap%60}m (< 8h required).",
                                (id1, id2)
                            ))
                            
    return conflicts


def display_schedule_audit(shifts, conflicts):
    """Renders formatted shift roster and itemized conflict audit."""
    border = "=" * 94
    dash = "-" * 94
    
    print("\n" + border)
    print(" " * 22 + "CAMPUS HOSPITAL & FACILITY MANAGEMENT")
    print(" " * 21 + "EMPLOYEE SHIFT SCHEDULE & CONFLICT AUDIT")
    print(border)
    print(f"{'Shift ID':<10}{'Emp ID':<10}{'Employee Name':<18}{'Day':<11}{'Start':<8}{'End':<8}{'Duration':<11}{'Department':<16}")
    print(dash)
    
    for s in shifts:
        s_id, e_id, name, day, s_str, e_str, dept = s
        s_min = parse_time_to_minutes(s_str)
        e_min = parse_time_to_minutes(e_str)
        dur_mins = e_min - s_min
        dur_str = f"{dur_mins//60}h {dur_mins%60:02d}m" if dur_mins > 0 else "INVALID"
        print(f"{s_id:<10}{e_id:<10}{name:<18}{day:<11}{s_str:<8}{e_str:<8}{dur_str:<11}{dept:<16}")
        
    print(dash)
    print(f"Total Shifts Scheduled: {len(shifts)} | Conflicts / Violations Detected: {len(conflicts)}")
    print(dash)
    
    if len(conflicts) > 0:
        print("[!] DETECTED SCHEDULE CONFLICTS & LABOUR VIOLATIONS:")
        idx = 1
        for conf in conflicts:
            category, details, involved = conf
            print(f"    [{idx}] CATEGORY: {category}")
            print(f"        Details : {details}")
            print(f"        Shifts  : {', '.join(involved)}")
            idx += 1
    else:
        print("[*] CLEAN SCHEDULE: Zero overlaps, adequate rest intervals, and compliant shift lengths.")
        
    print(border + "\n")


def run_demo():
    """Demonstration shift roster showcasing clean shifts, overlaps, rest violations, and duration violations."""
    shift_roster = [
        ("SH-101", "EMP-01", "Dr. A. Sharma",   "Monday", "08:00", "14:00", "Emergency"),
        ("SH-102", "EMP-01", "Dr. A. Sharma",   "Monday", "13:00", "19:00", "ICU Support"),       # Direct Overlap with SH-101 (13:00 < 14:00)
        ("SH-103", "EMP-02", "Nurse B. Devi",   "Monday", "07:00", "15:00", "General Ward"),
        ("SH-104", "EMP-02", "Nurse B. Devi",   "Monday", "19:00", "23:00", "Night Check"),       # Insufficient Rest (15:00 to 19:00 is 4h < 8h)
        ("SH-105", "EMP-03", "Tech C. Rao",     "Monday", "08:00", "20:00", "Radiology Lab"),     # 12h duration > 10h limit
        ("SH-106", "EMP-04", "Dr. D. Varma",    "Monday", "09:00", "17:00", "Cardiology"),        # Compliant single shift
        ("SH-107", "EMP-01", "Dr. A. Sharma",   "Tuesday", "09:00", "17:00", "OPD Clinic")        # Tuesday shift (different day - valid)
    ]
    
    conflicts = detect_shift_conflicts(shift_roster)
    display_schedule_audit(shift_roster, conflicts)


if __name__ == "__main__":
    run_demo()
