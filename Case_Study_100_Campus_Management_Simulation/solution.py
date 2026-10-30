"""Show sample student, event, and room information for a campus."""

def create_initial_campus_data():
    """
    Initializes mock database using lists and tuples (strictly adhering to syllabus).
    """
    # Student records: list of tuples
    # (roll_no, name, dept, [marks_sub1, sub2, sub3], attendance_pct, fee_paid)
    students = [
        ("26CSE001", "Aaditya Roy",    "CSE", [92.0, 88.0, 95.0], 88.0, True),
        ("26CSE002", "Bhavya Sri",     "CSE", [78.0, 72.0, 85.0], 82.0, True),
        ("26ECE001", "Charan Teja",    "ECE", [64.0, 58.0, 62.0], 68.5, False),  # Low attendance & fee due
        ("26ECE002", "Divya Reddy",    "ECE", [85.0, 90.0, 88.0], 91.0, True),
        ("26MEC001", "Eshwar Rao",     "MEC", [52.0, 48.0, 55.0], 71.0, True),   # Low attendance
        ("26INF001", "Fatima Zahra",   "INF", [88.0, 92.0, 90.0], 95.0, True)
    ]
    
    # Campus Events: list of tuples
    # (event_code, event_name, max_capacity, registered_rolls_list)
    events = [
        ("EVT-AI", "National AI & Robotics Symposium", 3, ["26CSE001", "26CSE002"]),
        ("EVT-HACK", "48-Hour Dussehra Hackathon", 2, ["26INF001"]),
        ("EVT-WKS", "Cloud Computing Workshop", 4, ["26ECE002", "26MEC001"])
    ]
    
    # Campus Labs/Venues: list of tuples
    # (venue_id, venue_name, capacity, bookings_list_of_tuples)
    # bookings_list: [(slot_str, booked_by_dept)]
    resources = [
        ("LAB-301", "Advanced Computing Lab", 60, [("09:00-11:00", "CSE"), ("14:00-16:00", "INF")]),
        ("AUD-101", "Sir C.V. Raman Auditorium", 250, [("10:00-13:00", "INSTITUTE")]),
        ("SEM-201", "ECE Seminar Hall", 80, [])
    ]
    
    return students, events, resources


def compute_student_academics(students):
    """
    Computes total marks, percentage, and grade for each student.
    Returns list of tuples: (roll, name, dept, total, pct, grade, att, fee_status, exam_eligible)
    """
    academic_report = []
    for s in students:
        roll, name, dept, marks, att, fee = s
        
        # Calculate sum and percentage
        total = 0.0
        for m in marks:
            total += m
        pct = round(total / len(marks), 2)
        
        # Grade computation
        if pct >= 90.0:
            grade = "O"
        elif pct >= 80.0:
            grade = "A+"
        elif pct >= 70.0:
            grade = "A"
        elif pct >= 60.0:
            grade = "B+"
        elif pct >= 50.0:
            grade = "B"
        elif pct >= 40.0:
            grade = "C"
        else:
            grade = "F"
            
        # Eligibility criteria: attendance >= 75% AND fee paid
        is_eligible = (att >= 75.0) and fee
        eligibility_str = "ELIGIBLE" if is_eligible else "BARRED"
        fee_str = "PAID" if fee else "DUE"
        
        academic_report.append((roll, name, dept, total, pct, grade, att, fee_str, eligibility_str))
        
    return academic_report


def display_academic_dashboard(academic_report):
    """Prints formatted student academic and examination eligibility table."""
    border = "=" * 94
    dash = "-" * 94
    print("\n" + border)
    print(" " * 26 + "STUDENT ACADEMIC & ELIGIBILITY REPORT")
    print(border)
    print(f"{'Roll No':<11}{'Student Name':<18}{'Dept':<6}{'Total':>8}{'Pct %':>8}{'Grade':>7}{'Att %':>8}{'Fee':>7}{'Exam Status':>14}")
    print(dash)
    
    for row in academic_report:
        roll, name, dept, total, pct, grade, att, fee, status = row
        print(f"{roll:<11}{name:<18}{dept:<6}{total:>8.1f}{pct:>7.1f}%{grade:>6}{att:>7.1f}%{fee:>7}  {status:>12}")
        
    print(dash)
    
    # Audit alerts
    barred_students = []
    for row in academic_report:
        if row[8] == "BARRED":
            barred_students.append(row)
            
    if len(barred_students) > 0:
        print("[!] EXAMINATION ADMIT CARD WITHHELD (BARRED DUE TO DEFICIENCIES):")
        for b in barred_students:
            reasons = []
            if b[6] < 75.0:
                reasons.append(f"Shortage of attendance ({b[6]:.1f}% < 75.0%)")
            if b[7] == "DUE":
                reasons.append("Semester tuition fee due")
            print(f"    - {b[1]} ({b[0]} - {b[2]}): {', '.join(reasons)}")
    else:
        print("[*] All students meet academic, attendance, and fee clearance standards.")
    print(border + "\n")


def register_student_for_event(events, event_code, roll_no):
    """
    Registers a student for a campus event respecting maximum capacity limits.
    """
    for e in events:
        code, name, max_cap, reg_list = e
        if code == event_code:
            if roll_no in reg_list:
                return False, f"Student {roll_no} is already registered for {name}."
            if len(reg_list) >= max_cap:
                return False, f"Registration failed! {name} has reached full capacity ({max_cap}/{max_cap})."
            reg_list.append(roll_no)
            return True, f"Success! {roll_no} registered for {name} ({len(reg_list)}/{max_cap} filled)."
    return False, f"Event code '{event_code}' not found."


def allocate_resource_slot(resources, venue_id, req_slot, dept):
    """
    Allocates a campus venue/lab for a department slot, detecting slot conflicts.
    """
    for res in resources:
        v_id, name, cap, bookings = res
        if v_id == venue_id:
            for b in bookings:
                slot, b_dept = b
                if slot == req_slot:
                    return False, f"Collision! {name} is already booked for slot '{req_slot}' by {b_dept} department."
            bookings.append((req_slot, dept))
            return True, f"Success! {name} reserved for {dept} during slot '{req_slot}'."
    return False, f"Venue ID '{venue_id}' not found."


def display_events_and_resources(events, resources):
    """Displays status of campus events and allocated laboratory resources."""
    dash = "-" * 88
    print("\n" + "=" * 88)
    print(" " * 24 + "CAMPUS EVENTS & CAPACITY DASHBOARD")
    print("=" * 88)
    print(f"{'Code':<11}{'Event Name':<38}{'Capacity':<12}{'Enrolled Roll Numbers'}")
    print(dash)
    for e in events:
        code, name, cap, reg_list = e
        enrolled_str = ", ".join(reg_list) if len(reg_list) > 0 else "[Empty]"
        cap_str = f"{len(reg_list)}/{cap}"
        print(f"{code:<11}{name:<38}{cap_str:<12}{enrolled_str}")
    print(dash)
    
    print("\n" + "=" * 88)
    print(" " * 22 + "CAMPUS VENUE & LAB RESOURCE SCHEDULE")
    print("=" * 88)
    print(f"{'Venue ID':<11}{'Venue Name':<32}{'Cap':>6}{'Active Bookings (Slot -> Dept)'}")
    print(dash)
    for r in resources:
        vid, vname, cap, bookings = r
        b_str = "; ".join([f"{slot} ({dept})" for slot, dept in bookings]) if len(bookings) > 0 else "[Available All Day]"
        print(f"{vid:<11}{vname:<32}{cap:>6}   {b_str}")
    print("=" * 88 + "\n")


def run_comprehensive_simulation():
    """Runs a complete end-to-end automated simulation test."""
    print("**********************************************************************************")
    print("   DR. RVR NRI INSTITUTE OF TECHNOLOGY - SMART CAMPUS MANAGEMENT SIMULATION")
    print("**********************************************************************************")
    
    # 1. Initialize data
    students, events, resources = create_initial_campus_data()
    
    # 2. Process academics
    academic_report = compute_student_academics(students)
    display_academic_dashboard(academic_report)
    
    # 3. Test Event Registration Logic
    print("[*] TESTING EVENT REGISTRATION SYSTEM:")
    # Test valid registration
    ok, msg = register_student_for_event(events, "EVT-HACK", "26CSE001")
    print(f"    - Attempt 1: {msg}")
    
    # Test capacity overflow (EVT-HACK capacity was 2, now full)
    ok, msg = register_student_for_event(events, "EVT-HACK", "26ECE001")
    print(f"    - Attempt 2 (Overflow Test): {msg}")
    
    # Test duplicate registration
    ok, msg = register_student_for_event(events, "EVT-AI", "26CSE001")
    print(f"    - Attempt 3 (Duplicate Test): {msg}")
    
    # 4. Test Resource Allocation Logic
    print("\n[*] TESTING LAB & VENUE RESOURCE SCHEDULER:")
    # Test booking collision on LAB-301 (already booked for 09:00-11:00)
    ok, msg = allocate_resource_slot(resources, "LAB-301", "09:00-11:00", "ECE")
    print(f"    - Booking Attempt 1 (Conflict Test): {msg}")
    
    # Test successful booking on open slot
    ok, msg = allocate_resource_slot(resources, "SEM-201", "11:00-13:00", "CSE")
    print(f"    - Booking Attempt 2 (Valid Slot)   : {msg}")
    
    # 5. Display consolidated final campus status
    display_events_and_resources(events, resources)
    print("**********************************************************************************")
    print("              SIMULATION COMPLETED SUCCESSFULLY WITH ZERO ERRORS                  ")
    print("**********************************************************************************\n")


if __name__ == "__main__":
    run_comprehensive_simulation()
