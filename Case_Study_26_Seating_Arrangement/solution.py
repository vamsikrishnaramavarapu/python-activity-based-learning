"""
Case Study 26: Nested Loop Examination Seating Generator
Syllabus Concepts: Computational Thinking, Variables, Data Types, Conditional Statements,
                   Nested Loops, Strings, Lists, Nested Lists, Tuples, and Tuple Unpacking.
"""

def create_hall_grid(rows, cols):
    """Initialize a 2D grid of size rows x cols with vacant desk indicators."""
    grid = []
    for r in range(rows):
        row_desks = []
        for c in range(cols):
            row_desks.append("[ VACANT ]")
        grid.append(row_desks)
    return grid


def is_adjacent_conflict(grid, r, c, dept, rows, cols):
    """
    Check if placing a student of department 'dept' at (r, c) causes
    an adjacent conflict (top, bottom, left, or right neighbor with same dept).
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbor = grid[nr][nc]
            # Neighbor format: "[CSE-101]" -> dept is prefix before hyphen
            if "-" in neighbor:
                # Extract dept substring
                clean = neighbor.replace("[", "").replace("]", "").strip()
                n_dept = clean.split("-")[0]
                if n_dept == dept:
                    return True
    return False


def generate_seating_arrangement(rows, cols, student_pool, reserved_coords):
    """
    Allocates seats using nested loops, alternate branch restrictions,
    and reserved seat preservation.
    student_pool: list of tuples (roll_no, dept, name)
    reserved_coords: list of tuples (r, c, reserve_label)
    """
    grid = create_hall_grid(rows, cols)
    
    # 1. Mark reserved seats
    for res in reserved_coords:
        rr, rc, label = res
        if 0 <= rr < rows and 0 <= rc < cols:
            grid[rr][rc] = f"[{label:^8}]"
            
    allocated_count = 0
    unallocated_students = []
    
    # Create an active working queue/list of students
    pending_students = []
    for s in student_pool:
        pending_students.append(s)
        
    # 2. Iterate through grid using nested loops to allocate seats
    for r in range(rows):
        for c in range(cols):
            # Skip if seat is already reserved
            if grid[r][c] != "[ VACANT ]":
                continue
                
            placed = False
            # Search pending students for a department that doesn't violate adjacent constraints
            for idx in range(len(pending_students)):
                roll_no, dept, name = pending_students[idx]
                
                if not is_adjacent_conflict(grid, r, c, dept, rows, cols):
                    # Valid placement found
                    seat_label = f"[{dept[:3]}-{roll_no[-3:]}]"
                    grid[r][c] = seat_label
                    allocated_count += 1
                    pending_students.pop(idx)
                    placed = True
                    break
                    
            if not placed and len(pending_students) > 0:
                # If no compatible student fits adjacency rule right now, leave desk vacant for separation
                grid[r][c] = "[ BUFFER ]"
                
    unallocated_students = pending_students
    return grid, allocated_count, unallocated_students


def display_hall_layout(grid, rows, cols, hall_name, capacity, allocated, unallocated):
    """Render a clean ASCII map of the examination hall."""
    border = "=" * (cols * 14 + 14)
    print("\n" + border)
    print(f"{hall_name.center(cols * 14 + 14)}")
    print(f"{'EXAMINATION SEATING MATRIX & AUDIT REPORT'.center(cols * 14 + 14)}")
    print(border)
    
    # Column Header
    header = f"{'Row / Col':<10}"
    for c in range(cols):
        header += f"   Col-{c+1:<3}   "
    print(header)
    print("-" * (cols * 14 + 14))
    
    # Print 2D Grid using nested loops
    for r in range(rows):
        row_str = f"Row-{r+1:<5} |"
        for c in range(cols):
            row_str += f" {grid[r][c]:^10} |"
        print(row_str)
        
    print("-" * (cols * 14 + 14))
    print(f"Hall Capacity      : {capacity} Desks ({rows} Rows x {cols} Columns)")
    print(f"Students Allocated : {allocated}")
    print(f"Desks Vacant/Buffer: {capacity - allocated}")
    print(f"Unallocated Count  : {len(unallocated)}")
    
    if len(unallocated) > 0:
        print("\n[!] WARNING: Unallocated Students (Capacity/Adjacency overflow):")
        for u in unallocated:
            roll, dept, name = u
            print(f"    - Roll: {roll} | Dept: {dept:<5} | Name: {name}")
    else:
        print("\n[*] SUCCESS: All students allocated adhering to alternate-branch constraints!")
    print(border + "\n")


def run_demo():
    """Execute seating generation demo for a 4x4 examination hall."""
    rows = 4
    cols = 4
    capacity = rows * cols
    
    # Reserved seats (row_idx, col_idx, reason_label)
    reserved = [
        (0, 0, "PWD-SEAT"),   # Physically challenged reserved desk
        (3, 3, "INVIG-BF")    # Invigilator reserve buffer
    ]
    
    # Mixed student candidates across CSE, ECE, MECH, and IT
    students = [
        ("26CSE101", "CSE", "Aarav Sharma"),
        ("26ECE201", "ECE", "Bhavna Patel"),
        ("26CSE102", "CSE", "Chaitanya Rao"),
        ("26ECE202", "ECE", "Deepa Verma"),
        ("26MEC301", "MEC", "Eashwar Reddy"),
        ("26INF401", "INF", "Farhan Akhtar"),
        ("26CSE103", "CSE", "Gautam Krishna"),
        ("26ECE203", "ECE", "Harika Devi"),
        ("26MEC302", "MEC", "Indrajit Paul"),
        ("26INF402", "INF", "Jaya Lakshmi"),
        ("26CSE104", "CSE", "Kalyan Varma"),
        ("26ECE204", "ECE", "Lavanya Nair"),
        ("26MEC303", "MEC", "Manoj Kumar"),
        ("26INF403", "INF", "Nandini Sen")
    ]
    
    grid, allocated, unallocated = generate_seating_arrangement(rows, cols, students, reserved)
    display_hall_layout(grid, rows, cols, "ROOM 302 - MAIN ACADEMIC BLOCK", capacity, allocated, unallocated)


if __name__ == "__main__":
    run_demo()
