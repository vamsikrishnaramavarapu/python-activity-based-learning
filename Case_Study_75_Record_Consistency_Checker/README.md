# Case Study 75: Integrated Student Record Consistency Checker

## 1. Problem Statement
Develop an integrated data consistency and integrity validation engine for institutional student databases. The system evaluates student records formatted as 6-element tuples `(roll_number, full_name, marks_tuple, attendance_percentage, fee_status, academic_standing)`. The program must systematically detect duplicate registration keys, validate alphanumeric syntax against university standards, audit numeric constraints (marks bounded within $[0.0, 100.0]$ and attendance bounded within $[0.0, 100.0]$), and trap contextual business logic contradictions (such as candidates awarded 'HONORS' standing despite deficient attendance or failing marks).

## 2. Objectives
- Ingest student profiles stored as composite tuples containing strings, nested tuples, floats, and booleans.
- Validate Roll Number Syntax: enforce exact length of 8 characters, verify 2-digit admission year prefix, valid department code (CSE/ECE/MEC/INF/CIV/EEE), and 3-digit serial suffix.
- Detect Duplicate Keys: maintain a historical tracking list to detect identity collisions across the database.
- Name Cleansing & Integrity: verify names contain at least 2 alphabetic characters and are free of illegal numeric symbols.
- Numerical Boundary Audits:
  - Verify every mark in the nested marks tuple satisfies $0.0 \le mark \le 100.0$.
  - Verify attendance percentage satisfies $0.0 \le att \le 100.0$.
- Rule Contradiction Trapping: detect logical inconsistencies, such as students classified under 'HONORS' standing who fail the minimum attendance threshold ($< 75\%$) or possess sub-par marks ($< 60.0$).
- Strict Syllabus Compliance: built purely with lists, tuples, nested tuples, tuple unpacking, string methods, loops, and conditional branching.

## 3. Assumptions
1. Each record is supplied as a tuple of 6 elements.
2. Marks are grouped in an immutable nested tuple.
3. Fee status is a boolean (`True` for paid, `False` for due).

## 4. Algorithm
1. **Initialize State:**
   - Create `seen_roll_numbers = []`, `clean_records = []`, `defect_log = []`.
2. **Record Validation Loop:**
   - For each record tuple `(roll_no, name, marks, att, fee, standing)`:
     - Initialize `entry_defects = []`.
     - **Check 1 (Roll Syntax):**
       - If length $\ne 8$ or year prefix is not numeric or dept code is unrecognized or serial is not numeric, record error.
       - If roll exists in `seen_roll_numbers`, record duplicate error; else append to `seen_roll_numbers`.
     - **Check 2 (Name):**
       - Strip spaces/dots; if length $< 2$ or contains non-alphabetic characters, record error.
     - **Check 3 (Marks Bounds):**
       - Verify marks is a tuple. For each mark $m$, if $m < 0.0$ or $m > 100.0$, record error.
     - **Check 4 (Attendance Bounds):**
       - If $att < 0.0$ or $att > 100.0$, record error.
     - **Check 5 (Academic Contradictions):**
       - If $standing == "HONORS"$:
         - If $\min(marks) < 60.0$ or $att < 75.0$, record contradiction defect.
     - **Verdict:**
       - If `entry_defects` is empty: append to `clean_records`.
       - Else: append defect details to `defect_log`.
3. **Display Output:**
   - Render clean records table followed by categorized integrity defect logs.

## 5. Flowchart
```mermaid
flowchart TD
    Start([Start]) --> InitLists[Init seen_rolls, clean_records, defect_log]
    InitLists --> LoopRecords{More Records in Database?}
    LoopRecords -- Yes --> UnpackRec[Unpack Roll, Name, Marks, Att, Fee, Standing]
    LoopRecords -- No --> DisplayAudit[Render Clean Table & Categorized Defect Report]
    DisplayAudit --> End([End])
    
    UnpackRec --> CheckRoll{Valid 8-Char Syntax & Known Branch?}
    CheckRoll -- No --> LogRollErr[Add Roll Syntax Error]
    CheckRoll -- Yes --> CheckDup{Roll in seen_rolls?}
    CheckDup -- Yes --> LogDupErr[Add Duplicate ID Error]
    CheckDup -- No --> SaveRoll[Add Roll to seen_rolls]
    
    LogRollErr --> CheckName
    LogDupErr --> CheckName
    SaveRoll --> CheckName{Valid Alphabetic Name?}
    
    CheckName -- No --> LogNameErr[Add Name Format Error]
    CheckName -- Yes --> CheckMarks{All Marks in [0, 100]?}
    LogNameErr --> CheckMarks
    
    CheckMarks -- No --> LogMarksErr[Add Marks Out-of-Bounds Error]
    CheckMarks -- Yes --> CheckAtt{Attendance in [0, 100]?}
    LogMarksErr --> CheckAtt
    
    CheckAtt -- No --> LogAttErr[Add Attendance Range Error]
    CheckAtt -- Yes --> CheckStanding{Standing == HONORS?}
    LogAttErr --> CheckStanding
    
    CheckStanding -- Yes --> CheckHonorsRules{Att >= 75% AND All Marks >= 60?}
    CheckStanding -- No --> CheckDefects
    CheckHonorsRules -- No --> LogHonorsErr[Add Academic Contradiction Error]
    CheckHonorsRules -- Yes --> CheckDefects
    LogHonorsErr --> CheckDefects
    
    CheckDefects{Any Defects Logged for Record?}
    CheckDefects -- Yes --> AddDefectList[Append to defect_log]
    CheckDefects -- No --> AddCleanList[Append to clean_records]
    AddDefectList --> LoopRecords
    AddCleanList --> LoopRecords
```

## 6. Pseudocode
```
BEGIN
    SET seen_rolls = []
    SET clean = []
    SET defects = []
    
    FOR EACH rec IN database DO
        UNPACK rec INTO (roll, name, marks, att, fee, standing)
        SET issues = []
        
        IF NOT VALID_ROLL(roll) THEN APPEND "Invalid Roll" TO issues
        ELSE IF roll IN seen_rolls THEN APPEND "Duplicate Roll" TO issues
        ELSE APPEND roll TO seen_rolls
        
        IF NOT VALID_NAME(name) THEN APPEND "Invalid Name" TO issues
        
        FOR EACH m IN marks DO
            IF m < 0 OR m > 100 THEN APPEND "Mark out of bounds" TO issues
        END FOR
        
        IF att < 0 OR att > 100 THEN APPEND "Attendance out of bounds" TO issues
        
        IF standing == "HONORS" AND (att < 75 OR MIN(marks) < 60) THEN
            APPEND "Honors contradiction" TO issues
        END IF
        
        IF LENGTH(issues) == 0 THEN
            APPEND rec TO clean
        ELSE
            APPEND (roll, issues) TO defects
        END IF
    END FOR
    
    OUTPUT clean table and defect report
END
```

## 7. Python Source Code
Refer to [solution.py](file:///c:/Users/vamsi/OneDrive/Desktop/python%20activity%20based%20learning/Case_Study_75_Record_Consistency_Checker/solution.py).

## 8. Test Cases
| Test ID | Record Sample | Detected Anomalies | Status |
|---|---|---|---|
| TC-01 | `("26CSE101", "Aaditya Roy", (92.0, 88.0, 95.0), 86.5, True, "HONORS")` | Clean Record -> Passes all rules | PASSED |
| TC-02 | `("26CSE101", "Bhavya Sri", ...)` | Duplicate Roll Number detected (26CSE101 repeated) | PASSED |
| TC-03 | `("XXXYZ999", "Charan Teja", ...)` | Roll Syntax Error: Year non-digit and branch code invalid | PASSED |
| TC-04 | `("26ECE201", "Divya Reddy", (-15.0, 85.0, 110.0), ...)` | Marks Bounds Error: Mark -15.0 and 110.0 out of [0, 100] | PASSED |
| TC-05 | `("26MEC301", "E1", ..., 108.5, ...)` | Name Error: contains digits; Attendance Error: 108.5% > 100% | PASSED |
| TC-06 | `("26INF401", "Farhan Akhtar", (88.0, 92.0, 90.0), 62.0, True, "HONORS")` | Contradiction Error: Marked HONORS but attendance is only 62.0% (< 75%) | PASSED |

## 9. Output Screenshot / Terminal Output
```
==============================================================================================
                      DR. RVR NRI INSTITUTE OF TECHNOLOGY
                    ACADEMIC DATABASE CONSISTENCY & INTEGRITY AUDIT
==============================================================================================
Total Raw Records Ingested : 7
Verified Consistent Records: 2 (28.6%)
Defective / Flagged Records: 5 (71.4%)
----------------------------------------------------------------------------------------------
VERIFIED CLEAN STUDENT RECORDS:
Roll No    Student Name        Marks                    Att %    Fee    Standing
----------------------------------------------------------------------------------------------
26CSE101   Aaditya Roy         (92.0, 88.0, 95.0)       86.5%   PAID        HONORS
26CSE102   Gautam Krishna      (78.0, 82.0, 79.0)       84.0%   PAID       REGULAR
----------------------------------------------------------------------------------------------
[!] INTEGRITY DEFECT & INCONSISTENCY LOG:
    - Record #2 (Ref: 26CSE101) | Type: INTEGRITY_VIOLATION
      Defects: DUPLICATE_ID: Roll number '26CSE101' has already been registered.
    - Record #3 (Ref: XXXYZ999) | Type: INTEGRITY_VIOLATION
      Defects: Roll Error: Year prefix (first 2) and serial (last 3) must be numeric digits.
    - Record #4 (Ref: 26ECE201) | Type: INTEGRITY_VIOLATION
      Defects: Marks Error: Mark -15.0 out of valid bounds [0.0, 100.0].
    - Record #5 (Ref: 26MEC301) | Type: INTEGRITY_VIOLATION
      Defects: Name Error: Name contains invalid non-alphabetic characters: 'E1'.; Attendance Error: Attendance 108.5% out of range [0.0, 100.0].
    - Record #6 (Ref: 26INF401) | Type: INTEGRITY_VIOLATION
      Defects: Contradiction: Student marked 'HONORS' but attendance is deficient (62.0% < 75%).
==============================================================================================
```

## 10. Conclusion
The integrated student record consistency checker provided thorough schema and semantic validation of student academic records. Utilizing tuples, nested tuples, string parsing, and boundary testing, the program successfully audited records without third-party frameworks.
