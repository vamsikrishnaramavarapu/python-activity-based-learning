"""Compare student answers with an answer key and calculate scores."""

def validate_answer_string(answer_str, expected_length):
    """
    Validates that student answer string matches expected length
    and contains only allowed characters ('A', 'B', 'C', 'D', 'X' for unattempted).
    """
    if len(answer_str) != expected_length:
        return False, f"Length mismatch: Expected {expected_length}, found {len(answer_str)}"
        
    valid_options = "ABCDX"
    for char in answer_str.upper():
        if char not in valid_options:
            return False, f"Invalid character detected: '{char}'. Only A, B, C, D, X permitted."
            
    return True, "Valid"


def evaluate_single_student(roll_no, student_name, student_answers, answer_key):
    """
    Evaluates a single student's answers against the master key.
    Marking scheme: +4 for correct, -1 for incorrect, 0 for unattempted ('X').
    Returns a result tuple.
    """
    answers = student_answers.upper()
    total_q = len(answer_key)
    correct = 0
    incorrect = 0
    unattempted = 0
    question_status = []  # List of 'C', 'I', 'U'
    
    for i in range(total_q):
        s_ans = answers[i]
        k_ans = answer_key[i]
        
        if s_ans == 'X':
            unattempted += 1
            question_status.append('U')
        elif s_ans == k_ans:
            correct += 1
            question_status.append('C')
        else:
            incorrect += 1
            question_status.append('I')
            
    max_marks = total_q * 4
    net_score = (correct * 4) - (incorrect * 1)
    attempted = correct + incorrect
    accuracy_pct = round((correct / attempted * 100), 2) if attempted > 0 else 0.0
    net_pct = round((net_score / max_marks * 100), 2)
    
    return (
        roll_no,
        student_name,
        correct,
        incorrect,
        unattempted,
        net_score,
        accuracy_pct,
        net_pct,
        question_status
    )


def sort_candidates_by_performance(results):
    """
    Sorts results in descending order of net_score.
    Tie-breaking rule: candidate with fewer negative marks (incorrect) ranks higher.
    Implemented purely using bubble sort to adhere strictly to syllabus.
    """
    n = len(results)
    sorted_list = []
    for item in results:
        sorted_list.append(item)
        
    for i in range(n - 1):
        for j in range(n - 1 - i):
            # Unpack tuples to compare
            r1_score = sorted_list[j][5]
            r1_incorrect = sorted_list[j][3]
            
            r2_score = sorted_list[j + 1][5]
            r2_incorrect = sorted_list[j + 1][3]
            
            # Condition to swap: lower score, or same score with MORE incorrect marks
            swap = False
            if r1_score < r2_score:
                swap = True
            elif r1_score == r2_score and r1_incorrect > r2_incorrect:
                swap = True
                
            if swap:
                temp = sorted_list[j]
                sorted_list[j] = sorted_list[j + 1]
                sorted_list[j + 1] = temp
                
    return sorted_list


def compute_question_analytics(evaluated_batch, total_questions):
    """
    Analyzes item difficulty: determines correct, incorrect, and skip count
    for each question across the student cohort.
    """
    analytics = []
    num_students = len(evaluated_batch)
    
    for q_idx in range(total_questions):
        c_count = 0
        i_count = 0
        u_count = 0
        for student in evaluated_batch:
            status_list = student[8]
            st = status_list[q_idx]
            if st == 'C':
                c_count += 1
            elif st == 'I':
                i_count += 1
            else:
                u_count += 1
        success_rate = round((c_count / num_students) * 100, 1) if num_students > 0 else 0.0
        analytics.append((q_idx + 1, c_count, i_count, u_count, success_rate))
        
    return analytics


def display_examination_report(answer_key, batch_records):
    """Displays full evaluation, ranked merit list, and question analytics."""
    total_q = len(answer_key)
    max_marks = total_q * 4
    evaluated_batch = []
    validation_errors = []
    
    # Process each student record
    for rec in batch_records:
        roll, name, ans_str = rec
        is_valid, msg = validate_answer_string(ans_str, total_q)
        if not is_valid:
            validation_errors.append((roll, name, msg))
            continue
        eval_tuple = evaluate_single_student(roll, name, ans_str, answer_key)
        evaluated_batch.append(eval_tuple)
        
    ranked_results = sort_candidates_by_performance(evaluated_batch)
    
    border = "=" * 92
    dash = "-" * 92
    
    print("\n" + border)
    print(" " * 22 + "NATIONAL ENTRANCE EXAMINATION SYSTEM")
    print(" " * 20 + "AUTOMATED ANSWER EVALUATION & MERIT AUDIT")
    print(border)
    print(f"Master Answer Key ({total_q} Questions): {answer_key}")
    print(f"Marking Scheme: Correct: +4 | Incorrect: -1 | Unanswered: 0 | Max Marks: {max_marks}")
    print(dash)
    
    # Print Ranked Merit Table
    print(f"{'Rank':<5}{'Roll No':<11}{'Student Name':<18}{'Correct':>8}{'Wrong':>7}{'Skip':>6}{'Net Score':>11}{'Accuracy':>10}{'Net %':>8}{'Result':>8}")
    print(dash)
    
    rank = 1
    for row in ranked_results:
        roll, name, c, w, u, net, acc, net_p, _ = row
        status = "QUALIFIED" if net >= (max_marks * 0.40) else "NEEDS IMPR"
        print(f"{rank:<5}{roll:<11}{name:<18}{c:>8}{w:>7}{u:>6}{net:>11}/{max_marks}{acc:>9.1f}%{net_p:>7.1f}%  {status}")
        rank += 1
        
    print(dash)
    
    if len(validation_errors) > 0:
        print("[!] DISQUALIFIED / MALFORMED ANSWER STRINGS DETECTED:")
        for err in validation_errors:
            eroll, ename, emsg = err
            print(f"    - Roll: {eroll} | Name: {ename} -> Reason: {emsg}")
        print(dash)
        
    # Question Analytics
    q_analytics = compute_question_analytics(evaluated_batch, total_q)
    print("\n[*] QUESTION-WISE DIFFICULTY & SUCCESS RATE ANALYTICS:")
    print(f"{'Q No':<6}{'Correct Count':>15}{'Wrong Count':>13}{'Skipped':>10}{'Success Rate':>15}{'Difficulty Classification':>28}")
    print("-" * 88)
    
    for qa in q_analytics:
        q_num, cc, wc, sc, s_rate = qa
        diff = "EASY" if s_rate >= 75.0 else ("MODERATE" if s_rate >= 40.0 else "HARD / FREQUENTLY MISSED")
        print(f"Q-{q_num:<4}{cc:>15}{wc:>13}{sc:>10}{s_rate:>14.1f}%  {diff:>26}")
        
    print(border + "\n")


def run_demo():
    """Run test cases with realistic entrance exam answer sheets."""
    # Official Master Answer Key for 15 questions
    official_key = "ABCDABCDABCDABC"
    
    students = [
        ("26ENG001", "Kavya Reddy",    "ABCDABCDABCDABC"),  # 100% perfect
        ("26ENG002", "Manoj Varma",    "ABCDABCDABCDXXX"),  # 12 attempted, all correct
        ("26ENG003", "Naveen Kumar",   "ABCDABCDABCDABA"),  # 1 wrong at end
        ("26ENG004", "Pooja Sharma",   "A BCDABCDABCDABC"), # Length 16 (error!)
        ("26ENG005", "Rajesh Gupta",   "ABCDABCDABCDABZ"),  # Invalid char 'Z' (error!)
        ("26ENG006", "Sneha Patel",    "BACDBACDBACDBAC"),  # High error rate
        ("26ENG007", "Teja Vardhan",   "ABCDABCDABCDABA")   # Tied with Naveen Kumar
    ]
    
    display_examination_report(official_key, students)


if __name__ == "__main__":
    run_demo()
