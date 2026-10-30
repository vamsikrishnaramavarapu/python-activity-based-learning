"""
Case Study 56: Student Group Formation with Score Balancing Engine
Syllabus Concepts: Computational Thinking, Variables, Operators, Conditional Statements,
                   Loops, Lists, Nested Lists, Tuples, and Tuple Unpacking.
"""

def bubble_sort_students_descending(student_list):
    """
    Sorts a list of student tuples (std_id, name, score)
    in descending order of score using bubble sort.
    """
    sorted_students = []
    for s in student_list:
        sorted_students.append(s)
        
    n = len(sorted_students)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            # Unpack scores to compare
            id1, name1, score1 = sorted_students[j]
            id2, name2, score2 = sorted_students[j + 1]
            if score1 < score2:
                # Swap elements
                temp = sorted_students[j]
                sorted_students[j] = sorted_students[j + 1]
                sorted_students[j + 1] = temp
                
    return sorted_students


def allocate_serpentine_groups(sorted_students, num_groups):
    """
    Allocates sorted students into num_groups using a Serpentine (Snake Draft) algorithm.
    Round 1: 0, 1, ..., K-1
    Round 2: K-1, K-2, ..., 0
    Round 3: 0, 1, ..., K-1
    This mathematically minimizes the disparity between team total scores.
    """
    groups = []
    for _ in range(num_groups):
        groups.append([])
        
    current_team_idx = 0
    direction = 1  # 1 for forward, -1 for reverse
    
    for student in sorted_students:
        groups[current_team_idx].append(student)
        
        # Advance index based on current serpentine direction
        if direction == 1:
            if current_team_idx == num_groups - 1:
                # Reached the right boundary: reverse direction for next allocation
                direction = -1
            else:
                current_team_idx += 1
        else:
            if current_team_idx == 0:
                # Reached the left boundary: reverse direction for next allocation
                direction = 1
            else:
                current_team_idx -= 1
                
    return groups


def compute_group_metrics(groups):
    """
    Calculates total score, average score, min, max, and count for each group.
    Returns (group_stats, overall_disparity)
    """
    group_stats = []
    totals = []
    
    for g_idx in range(len(groups)):
        roster = groups[g_idx]
        total_score = 0.0
        min_score = 1000.0
        max_score = -1.0
        
        for std in roster:
            _, _, score = std
            total_score += score
            if score < min_score:
                min_score = score
            if score > max_score:
                max_score = score
                
        count = len(roster)
        avg_score = round(total_score / count, 2) if count > 0 else 0.0
        totals.append(total_score)
        
        group_stats.append((
            g_idx + 1,
            count,
            round(total_score, 1),
            avg_score,
            min_score if count > 0 else 0.0,
            max_score if count > 0 else 0.0,
            roster
        ))
        
    # Overall cohort score spread
    highest_team_total = totals[0]
    lowest_team_total = totals[0]
    for t in totals:
        if t > highest_team_total:
            highest_team_total = t
        if t < lowest_team_total:
            lowest_team_total = t
            
    disparity = round(highest_team_total - lowest_team_total, 2)
    return group_stats, disparity


def display_balanced_groups_report(group_stats, disparity, num_groups):
    """Prints a structured team allocation report and fairness audit."""
    border = "=" * 90
    dash = "-" * 90
    
    print("\n" + border)
    print(" " * 22 + "CAMPUS HACKATHON & PROJECT SELECTION")
    print(" " * 20 + "SERPENTINE SCORE-BALANCED GROUP ALLOCATION")
    print(border)
    print(f"Target Number of Teams : {num_groups} Teams")
    print(f"Maximum Total Disparity: {disparity} points between highest and lowest team totals")
    print(dash)
    
    for stat in group_stats:
        team_num, count, total, avg, min_s, max_s, roster = stat
        print(f"\nTEAM #{team_num:<2} | Members: {count} | Total Score: {total:>6.1f} | Avg Score: {avg:>5.2f} | Range: [{min_s} - {max_s}]")
        print(f"{'  Roll ID':<12}{'Student Name':<22}{'Score':>8}")
        print("  " + "-" * 42)
        for std in roster:
            s_id, name, score = std
            print(f"  {s_id:<10}{name:<22}{score:>8.1f}")
            
    print("\n" + dash)
    print("SUMMARY COMPARATIVE SCORE TABLE:")
    print(f"{'Team ID':<10}{'Member Count':>15}{'Total Score':>15}{'Average Score':>15}{'Balance Status':>20}")
    print(dash)
    for stat in group_stats:
        team_num, count, total, avg, _, _, _ = stat
        status = "WELL-BALANCED" if disparity <= 10.0 else "ACCEPTABLE"
        print(f"Team {team_num:<5}{count:>15}{total:>15.1f}{avg:>15.2f}{status:>20}")
    print(border + "\n")


def run_demo():
    """Demonstrate score balancing on 16 students into 4 balanced teams."""
    students = [
        ("26CS01", "Aaditya Roy",    98.5),
        ("26CS02", "Bhavya Sri",     95.0),
        ("26CS03", "Charan Teja",    92.0),
        ("26CS04", "Divya Reddy",    89.0),
        ("26CS05", "Eshwar Rao",     86.5),
        ("26CS06", "Fatima Zahra",   84.0),
        ("26CS07", "Gautam Krishna", 81.5),
        ("26CS08", "Harika Devi",    78.0),
        ("26CS09", "Indrajit Paul",  75.5),
        ("26CS10", "Jaya Lakshmi",   72.0),
        ("26CS11", "Kalyan Varma",   69.0),
        ("26CS12", "Lavanya Nair",   66.5),
        ("26CS13", "Manoj Kumar",    63.0),
        ("26CS14", "Nandini Sen",    59.5),
        ("26CS15", "Omkar Nath",     55.0),
        ("26CS16", "Pooja Hegde",    50.0)
    ]
    
    num_teams = 4
    sorted_std = bubble_sort_students_descending(students)
    groups = allocate_serpentine_groups(sorted_std, num_teams)
    stats, disparity = compute_group_metrics(groups)
    display_balanced_groups_report(stats, disparity, num_teams)


if __name__ == "__main__":
    run_demo()
