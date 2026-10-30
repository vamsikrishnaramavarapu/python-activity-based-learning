# Case Study 91: Advanced String-Based Registration Record Analyzer

## 1. Problem Statement
Develop a lexical analysis and parsing engine to ingest raw structured student admission strings formatted using custom multi-segment delimiters. The system must parse delimited payloads formatted as `"REG#YYYY-DEPT-XXXX|NAME:Full_Name|DOB:YYYY-MM-DD|CATEGORY:Category|STATUS:Status"`, validate segment counts, enforce sub-token grammar (admission year, valid departmental codes, numeric sequence IDs, valid Gregorian calendar dates, enumerated reservation categories, and admission statuses), extract normalized records into immutable structured tuples, prevent duplicate keys, and classify syntax defects into formal error classes.

## 2. Objectives
- Tokenize raw input strings using the pipe delimiter (`'|'`) into exact 5-field records.
- Deconstruct and validate the registration token:
  - Check for mandatory prefix `'REG#'`.
  - Validate year token (4-digit numeric string).
  - Verify department code against allowed academic branches: `['CSE', 'ECE', 'MEC', 'INF', 'CIV', 'EEE']`.
  - Validate 4-digit serial identifier.
- Parse and sanitize candidate full name: replace underscores with spaces and ensure non-empty alphabetic content.
- Validate Date of Birth (DOB): verify `YYYY-MM-DD` syntax, check year within student bounds $[1995, 2012]$, month $[1, 12]$, and day $[1, 31]$.
- Enforce enumeration constraints:
  - Categories: `GENERAL`, `OBC`, `SC`, `ST`, `EWS`.
  - Statuses: `CONFIRMED`, `PROVISIONAL`, `WAITLISTED`.
- Identify duplicate registration identifiers using sequence membership tracking.
- Output clean structured database table alongside categorized error diagnostics.

## 3. Assumptions
1. Input records are supplied as single-line ASCII strings.
2. Underscores in the name field denote word spacing.
3. Gregorian calendar month lengths are bounded by general numeric ranges without complex leap year exceptions.

## 4. Algorithm
1. **Delimiter Check:**
   - Split input string by `'|'`.
   - If token count $\ne 5$, return `DELIMITER_ERROR`.
2. **Field Parsing & Validation:**
   - **Token 0 (Registration):** Must start with `'REG#'`. Split suffix by `'-'`. Verify year length $4$, dept code in whitelist, serial length $4$.
   - **Token 1 (Name):** Must start with `'NAME:'`. Slice value. Replace `'_'` with `' '`. Verify alphabetic content.
   - **Token 2 (DOB):** Must start with `'DOB:'`. Split by `'-'`. Verify year, month $\in [1, 12]$, day $\in [1, 31]$.
   - **Token 3 (Category):** Must start with `'CATEGORY:'`. Value must be in `['GENERAL', 'OBC', 'SC', 'ST', 'EWS']`.
   - **Token 4 (Status):** Must start with `'STATUS:'`. Value must be in `['CONFIRMED', 'PROVISIONAL', 'WAITLISTED']`.
3. **Duplicate Detection:**
   - If registration key already exists in `seen_ids`, flag `DUPLICATE_KEY_ERROR`.
   - Else, register key and pack parsed fields into tuple: `(reg_id, year, dept, seq, name, dob, cat, stat)`.
4. **Display:**
   - Print parsed table followed by itemized error diagnosis.

## 5. Flowchart
```mermaid
flowchart TD
    Start([Start]) --> NextLine{More Raw Strings to Parse?}
    NextLine -- Yes --> SplitTokens[Split String by Pipe Delimiter '|']
    NextLine -- No --> RenderAudit[Display Parsed Table & Error Logs]
    RenderAudit --> End([End])
    
    SplitTokens --> CheckTokenCount{Exactly 5 Tokens?}
    CheckTokenCount -- No --> LogDelimError[Log DELIMITER_ERROR]
    LogDelimError --> NextLine
    
    CheckTokenCount -- Yes --> ValidateRegToken{Validate REG# Token Syntax & Branch}
    ValidateRegToken -- Invalid --> LogRegError[Log REG_ID_ERROR]
    LogRegError --> NextLine
    
    ValidateRegToken -- Valid --> ValidateName{Validate NAME: & Alphabetic Characters}
    ValidateName -- Invalid --> LogNameError[Log NAME_SYNTAX_ERROR]
    LogNameError --> NextLine
    
    ValidateName -- Valid --> ValidateDOB{Validate DOB: YYYY-MM-DD Bounds}
    ValidateDOB -- Invalid --> LogDOBError[Log DATE_ERROR]
    LogDOBError --> NextLine
    
    ValidateDOB -- Valid --> ValidateEnums{Validate Category & Status Enums}
    ValidateEnums -- Invalid --> LogEnumError[Log ENUM_ERROR]
    LogEnumError --> NextLine
    
    ValidateEnums -- Valid --> CheckDupID{Reg ID Already in seen_ids?}
    CheckDupID -- Yes --> LogDupKey[Log DUPLICATE_KEY_ERROR]
    CheckDupID -- No --> PackValidTuple[Append ID to seen_ids & Pack Valid Tuple]
    LogDupKey --> NextLine
    PackValidTuple --> NextLine
```

## 6. Pseudocode
```
BEGIN
    SET parsed_list = []
    SET errors = []
    SET seen_ids = []
    
    FOR EACH line IN raw_records DO
        tokens = SPLIT(line, "|")
        IF LENGTH(tokens) != 5 THEN
            APPEND "DELIMITER_ERROR" TO errors
            CONTINUE
        END IF
        
        IF NOT PARSE_REG(tokens[0]) THEN APPEND "REG_ID_ERROR" TO errors; CONTINUE
        IF NOT PARSE_NAME(tokens[1]) THEN APPEND "NAME_ERROR" TO errors; CONTINUE
        IF NOT PARSE_DOB(tokens[2]) THEN APPEND "DATE_ERROR" TO errors; CONTINUE
        IF NOT PARSE_CAT(tokens[3]) THEN APPEND "CAT_ERROR" TO errors; CONTINUE
        IF NOT PARSE_STAT(tokens[4]) THEN APPEND "STAT_ERROR" TO errors; CONTINUE
        
        reg_id = EXTRACT_REG(tokens[0])
        IF reg_id IN seen_ids THEN
            APPEND "DUPLICATE_KEY_ERROR" TO errors
        ELSE
            APPEND reg_id TO seen_ids
            APPEND TUPLE(reg_id, name, dob, cat, stat) TO parsed_list
        END IF
    END FOR
    
    OUTPUT parsed table and error report
END
```

## 7. Python Source Code
Refer to [solution.py](file:///c:/Users/vamsi/OneDrive/Desktop/python%20activity%20based%20learning/Case_Study_91_Registration_Analyzer/solution.py).

## 8. Test Cases
| Test ID | Raw String Input | Expected Behavior | Status |
|---|---|---|---|
| TC-01 | `"REG#2026-CSE-0142\|NAME:Aditya_Sharma\|DOB:2006-05-14\|CATEGORY:GENERAL\|STATUS:CONFIRMED"` | Successfully parsed into valid 8-element tuple | PASSED |
| TC-02 | `"REG#2026-CSE-0143\|NAME:Charan_Teja\|DOB:2006-02-10"` | Delimiter Error: Expected 5 fields, found 3 | PASSED |
| TC-03 | `"REG#2026-BIO-0999\|..."` | Reg ID Error: Invalid dept code 'BIO' | PASSED |
| TC-04 | `"...\|DOB:2006-14-05\|..."` | Date Error: Month 14 out of valid range [1 - 12] | PASSED |
| TC-05 | Second occurrence of `"REG#2026-CSE-0142"` | Duplicate Key Error: Duplicate registration identifier detected | PASSED |

## 9. Output Screenshot / Terminal Output
```
==================================================================================================
                        DR. RVR NRI INSTITUTE OF TECHNOLOGY
                      CAMPUS ADMISSION REGISTRATION STRING ANALYZER
==================================================================================================
Total Strings Processed: 7
Successfully Extracted : 3
Rejected / Malformed   : 4
--------------------------------------------------------------------------------------------------
PARSED STRUCTURED REGISTRATION DATABASE:
Reg ID             Dept  Year  Candidate Name        DOB         Category  Status      
--------------------------------------------------------------------------------------------------
REG#2026-CSE-0142  CSE   2026  Aditya Sharma         2006-05-14  GENERAL   CONFIRMED   
REG#2026-ECE-0205  ECE   2026  Bhavya Sri Reddy      2005-11-20  OBC       PROVISIONAL 
REG#2026-MEC-0315  MEC   2026  Fatima Zahra          2006-09-30  EWS       CONFIRMED   
--------------------------------------------------------------------------------------------------
[!] PARSING DEFECT CLASSIFICATION & AUDIT LOG:
    - Entry #3 | Defect Class: DELIMITER_ERROR     
      Reason: Expected 5 pipe-delimited fields, found 3
      Raw   : "REG#2026-CSE-0143|NAME:Charan_Teja|DOB:2006-02-10"
    - Entry #4 | Defect Class: REG_ID_ERROR        
      Reason: Invalid department code 'BIO'. Must be one of ['CSE', 'ECE', 'MEC', 'INF', 'CIV', 'EEE'].
      Raw   : "REG#2026-BIO-0999|NAME:Divya_Rao|DOB:2005-08-15|CATEGORY:SC|STATUS:CONFIRMED"
    - Entry #5 | Defect Class: DATE_ERROR          
      Reason: Month 14 out of valid range [1 - 12].
      Raw   : "REG#2026-INF-0410|NAME:Eshwar_Prasad|DOB:2006-14-05|CATEGORY:ST|STATUS:CONFIRMED"
    - Entry #6 | Defect Class: DUPLICATE_KEY_ERROR 
      Reason: Duplicate registration identifier 'REG#2026-CSE-0142' detected.
      Raw   : "REG#2026-CSE-0142|NAME:Another_Student|DOB:2006-01-01|CATEGORY:GENERAL|STATUS:WAITLISTED"
==================================================================================================
```

## 10. Conclusion
The advanced string registration analyzer demonstrated comprehensive parsing and grammar validation of unstructured input strings. Using built-in string methods, slicing, lists, and tuples, it cleanly separated well-formed records from defective inputs according to academic specifications.
