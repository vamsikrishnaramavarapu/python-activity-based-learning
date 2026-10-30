# Case Study 48: Tuple-Based Employee Shift Conflict Detection

## 1. Problem Statement
Develop an employee duty schedule and labor compliance verification engine using immutable tuples to represent shifts. The program must ingest shift records in the form `(shift_id, employee_id, employee_name, day, start_time, end_time, department)`, convert 24-hour time strings into absolute temporal minute offsets, and execute pairwise conflict analysis to detect concurrent schedule overlaps, insufficient inter-shift rest intervals (< 8 hours), and shifts exceeding maximum allowable shift duration (> 10 hours).

## 2. Objectives
- Model shift records as immutable 7-element tuples: `(shift_id, emp_id, emp_name, day, start_str, end_str, dept)`.
- Convert 24-hour time strings (`"HH:MM"`) into integer minutes from midnight using string slicing/splitting and arithmetic operators.
- Implement Interval Collision Detection: for any two shifts assigned to the same employee on the same day, detect temporal overlap where:
  $$\max(Start_1, Start_2) < \min(End_1, End_2)$$
- Check Minimum Rest Gap: verify that the idle gap between consecutive shifts on the same day is $\ge 480$ minutes (8 hours).
- Enforce Shift Duration Upper Bound: flag any individual shift exceeding 600 minutes (10 hours).
- Adhere strictly to the syllabus using tuples, tuple unpacking, nested loops, conditional branches, and custom procedural algorithms.

## 3. Assumptions
1. Shift timings are represented in 24-hour format `"HH:MM"` within a single calendar day ($00:00$ to $23:59$).
2. Shift ID is unique per assignment.
3. Employee records are compared pairwise across matching calendar days.

## 4. Algorithm
1. **Time Parsing:**
   - Split `"HH:MM"` by separator `':'` to yield $H$ and $M$.
   - Compute total minutes $= H \times 60 + M$.
2. **Single-Shift Duration Verification:**
   - For each shift tuple:
     - Compute $duration = End - Start$.
     - If $duration \le 0$, log `INVALID_TIMING`.
     - Else if $duration > 600$ minutes, log `EXCESSIVE_DURATION`.
3. **Pairwise Conflict Analysis:**
   - For $i$ from $0$ to $N - 1$:
     - For $j$ from $i + 1$ to $N - 1$:
       - Unpack tuples $s_1$ and $s_2$.
       - If $emp_1 == emp_2$ AND $day_1 == day_2$:
         - Let $O_{start} = \max(start_1, start_2)$, $O_{end} = \min(end_1, end_2)$.
         - If $O_{start} < O_{end}$:
           - Overlap detected with duration $O_{end} - O_{start}$. Append `DIRECT_OVERLAP` conflict.
         - Else:
           - If $end_1 \le start_2$: $gap = start_2 - end_1$.
           - Else: $gap = start_1 - end_2$.
           - If $gap < 480$:
             - Append `INSUFFICIENT_REST` conflict.
4. **Output Report:**
   - Print formatted shift schedule table and detailed itemized audit logs.

## 5. Flowchart
```mermaid
flowchart TD
    Start([Start]) --> LoadShifts[Load List of Shift Tuples]
    LoadShifts --> SingleShiftLoop{For Each Shift in Roster}
    SingleShiftLoop -- Check Duration --> ParseMin[Parse Start and End Times to Minutes]
    ParseMin --> DurCheck{Duration > 10 Hours OR <= 0?}
    DurCheck -- Yes --> LogDurViolation[Log Duration / Invalid Timing Violation]
    DurCheck -- No --> NextSingle[Next Shift]
    LogDurViolation --> NextSingle
    NextSingle --> SingleShiftLoop
    
    SingleShiftLoop -- All Single Shifts Audited --> OuterLoop{For Shift i = 0 to N - 1}
    OuterLoop -- Next i --> InnerLoop{For Shift j = i + 1 to N - 1}
    OuterLoop -- Done --> RenderReport[Display Shift Table & Itemized Conflict Log]
    RenderReport --> End([End])
    
    InnerLoop -- Next j --> SameEmpDay{Same Employee & Same Day?}
    InnerLoop -- Inner Done --> OuterLoop
    SameEmpDay -- No --> InnerLoop
    SameEmpDay -- Yes --> CheckOverlap{max(s1, s2) < min(e1, e2)?}
    
    CheckOverlap -- Yes (Overlap) --> LogOverlap[Log DIRECT_OVERLAP Violation]
    LogOverlap --> InnerLoop
    
    CheckOverlap -- No --> CheckRest{Rest Interval < 8 Hours (480 mins)?}
    CheckRest -- Yes --> LogRest[Log INSUFFICIENT_REST Violation]
    CheckRest -- No --> InnerLoop
    LogRest --> InnerLoop
```

## 6. Pseudocode
```
BEGIN
    FUNCTION TO_MINUTES(time_str):
        parts = SPLIT(time_str, ":")
        RETURN (INTEGER(parts[0]) * 60) + INTEGER(parts[1])
    END FUNCTION

    FOR EACH shift IN roster:
        UNPACK shift INTO (id, emp, name, day, s_str, e_str, dept)
        dur = TO_MINUTES(e_str) - TO_MINUTES(s_str)
        IF dur > 600 THEN LOG "EXCESSIVE_DURATION"
    END FOR

    FOR i FROM 0 TO N - 1 DO
        FOR j FROM i + 1 TO N - 1 DO
            UNPACK roster[i] INTO (id1, emp1, name1, day1, s1, e1, d1)
            UNPACK roster[j] INTO (id2, emp2, name2, day2, s2, e2, d2)
            
            IF emp1 == emp2 AND day1 == day2 THEN
                IF MAX(s1, s2) < MIN(e1, e2) THEN
                    LOG "DIRECT_OVERLAP"
                ELSE
                    gap = (e1 <= s2) ? (s2 - e1) : (s1 - e2)
                    IF gap < 480 THEN LOG "INSUFFICIENT_REST"
                END IF
            END IF
        END FOR
    END FOR
    
    DISPLAY roster and conflict alerts
END
```

## 7. Python Source Code
Refer to [solution.py](file:///c:/Users/vamsi/OneDrive/Desktop/python%20activity%20based%20learning/Case_Study_48_Shift_Conflict_Detector/solution.py).

## 8. Test Cases
| Test ID | Scenario | Expected Violation | Status |
|---|---|---|---|
| TC-01 | SH-101 (08:00–14:00) vs SH-102 (13:00–19:00) for Dr. A. Sharma | Direct Overlap of 60 minutes detected | PASSED |
| TC-02 | SH-103 (07:00–15:00) vs SH-104 (19:00–23:00) for Nurse B. Devi | Insufficient rest detected (gap is 4h 0m < 8h required) | PASSED |
| TC-03 | SH-105 (08:00–20:00, 12 hours) for Tech C. Rao | Excessive duration detected (12h > 10h statutory limit) | PASSED |
| TC-04 | SH-106 (09:00–17:00) on Monday vs SH-107 on Tuesday for Dr. Sharma | Different day / compliant single shift -> No conflict | PASSED |

## 9. Output Screenshot / Terminal Output
```
==============================================================================================
                      CAMPUS HOSPITAL & FACILITY MANAGEMENT
                     EMPLOYEE SHIFT SCHEDULE & CONFLICT AUDIT
==============================================================================================
Shift ID  Emp ID    Employee Name     Day        Start   End     Duration   Department      
----------------------------------------------------------------------------------------------
SH-101    EMP-01    Dr. A. Sharma     Monday     08:00   14:00   6h 00m     Emergency       
SH-102    EMP-01    Dr. A. Sharma     Monday     13:00   19:00   6h 00m     ICU Support     
SH-103    EMP-02    Nurse B. Devi     Monday     07:00   15:00   8h 00m     General Ward    
SH-104    EMP-02    Nurse B. Devi     Monday     19:00   23:00   4h 00m     Night Check     
SH-105    EMP-03    Tech C. Rao       Monday     08:00   20:00   12h 00m    Radiology Lab   
SH-106    EMP-04    Dr. D. Varma      Monday     09:00   17:00   8h 00m     Cardiology      
SH-107    EMP-01    Dr. A. Sharma     Tuesday    09:00   17:00   8h 00m     OPD Clinic      
----------------------------------------------------------------------------------------------
Total Shifts Scheduled: 7 | Conflicts / Violations Detected: 3
----------------------------------------------------------------------------------------------
[!] DETECTED SCHEDULE CONFLICTS & LABOUR VIOLATIONS:
    [1] CATEGORY: EXCESSIVE_DURATION
        Details : Shift SH-105 for Tech C. Rao (EMP-03) on Monday exceeds maximum daily work limit: 12h 0m > 10h limit.
        Shifts  : SH-105
    [2] CATEGORY: DIRECT_OVERLAP
        Details : Collision between SH-101 (08:00-14:00) and SH-102 (13:00-19:00) for Dr. A. Sharma (EMP-01) on Monday. Overlap: 60 mins.
        Shifts  : SH-101, SH-102
    [3] CATEGORY: INSUFFICIENT_REST
        Details : Rest violation between SH-103 and SH-104 for Nurse B. Devi on Monday: Rest gap is only 4h 0m (< 8h required).
        Shifts  : SH-103, SH-104
==============================================================================================
```

## 10. Conclusion
The tuple-based shift conflict detector utilized tuple immutability, tuple unpacking, and interval arithmetic to evaluate hospital work schedules. The program successfully flagged direct overlaps, inadequate rest, and overtime breaches using only fundamental Python syllabus elements.
