"""
Case Study 91: Advanced String-Based Registration Record Analyzer
Syllabus Concepts: Computational Thinking, Variables, Operators, Conditional Statements,
                   Loops, Strings, String Slicing & Methods, Lists, Tuples, and Tuple Unpacking.
"""

def parse_and_validate_date(dob_str):
    """
    Validates DOB string in format YYYY-MM-DD.
    Returns (is_valid, error_msg).
    """
    parts = dob_str.split("-")
    if len(parts) != 3:
        return False, f"Malformed date structure '{dob_str}'. Expected YYYY-MM-DD."
        
    y_str, m_str, d_str = parts
    if not (y_str.isdigit() and m_str.isdigit() and d_str.isdigit()):
        return False, f"Non-numeric date component in '{dob_str}'."
        
    year = int(y_str)
    month = int(m_str)
    day = int(d_str)
    
    if year < 1995 or year > 2012:
        return False, f"Birth year {year} outside valid student age bracket [1995 - 2012]."
    if month < 1 or month > 12:
        return False, f"Month {month} out of valid range [1 - 12]."
    if day < 1 or day > 31:
        return False, f"Day {day} out of valid range [1 - 31]."
        
    return True, "Valid"


def parse_registration_token(token):
    """
    Parses 'REG#YYYY-DEPT-XXXX'
    Returns (is_valid, error_msg, year, dept, seq).
    """
    if not token.startswith("REG#"):
        return False, "Missing 'REG#' prefix", "", "", ""
        
    body = token[4:]  # Slice off 'REG#'
    segments = body.split("-")
    if len(segments) != 3:
        return False, f"Registration identifier '{body}' must have 3 hyphen-separated segments (YYYY-DEPT-XXXX)", "", "", ""
        
    year_str, dept_str, seq_str = segments
    if not (year_str.isdigit() and len(year_str) == 4):
        return False, f"Invalid admission year '{year_str}'. Expected 4 digits.", "", "", ""
    if not (seq_str.isdigit() and len(seq_str) == 4):
        return False, f"Invalid sequence serial '{seq_str}'. Expected 4 digits.", "", "", ""
        
    valid_depts = ["CSE", "ECE", "MEC", "INF", "CIV", "EEE"]
    dept_upper = dept_str.upper()
    if dept_upper not in valid_depts:
        return False, f"Invalid department code '{dept_str}'. Must be one of {valid_depts}.", "", "", ""
        
    return True, "Valid", year_str, dept_upper, seq_str


def analyze_raw_registration_string(raw_line):
    """
    Parses raw delimited string:
    'REG#YYYY-DEPT-XXXX|NAME:Aditya_Sharma|DOB:YYYY-MM-DD|CATEGORY:GENERAL|STATUS:CONFIRMED'
    Returns (is_valid, result_tuple_or_error_tuple).
    """
    cleaned = raw_line.strip()
    if len(cleaned) == 0:
        return False, ("EMPTY_RECORD", "Line is completely empty", raw_line)
        
    tokens = cleaned.split("|")
    if len(tokens) != 5:
        return False, ("DELIMITER_ERROR", f"Expected 5 pipe-delimited fields, found {len(tokens)}", raw_line)
        
    t_reg, t_name, t_dob, t_cat, t_stat = tokens
    
    # 1. Registration ID validation
    is_reg_ok, reg_msg, year, dept, seq = parse_registration_token(t_reg.strip())
    if not is_reg_ok:
        return False, ("REG_ID_ERROR", reg_msg, raw_line)
        
    # 2. Name token validation
    if not t_name.strip().startswith("NAME:"):
        return False, ("NAME_FIELD_ERROR", "Field 2 must start with 'NAME:'", raw_line)
    raw_name = t_name.strip()[5:]
    if len(raw_name) < 2:
        return False, ("NAME_SYNTAX_ERROR", "Name cannot be empty or less than 2 characters", raw_line)
    # Check that name only contains letters and underscores
    for ch in raw_name:
        if not (ch.isalpha() or ch == '_' or ch == ' '):
            return False, ("NAME_SYNTAX_ERROR", f"Illegal character '{ch}' in name field", raw_line)
    clean_name = raw_name.replace("_", " ")
    
    # 3. DOB token validation
    if not t_dob.strip().startswith("DOB:"):
        return False, ("DOB_FIELD_ERROR", "Field 3 must start with 'DOB:'", raw_line)
    dob_val = t_dob.strip()[4:]
    is_dob_ok, dob_msg = parse_and_validate_date(dob_val)
    if not is_dob_ok:
        return False, ("DATE_ERROR", dob_msg, raw_line)
        
    # 4. Category token validation
    if not t_cat.strip().startswith("CATEGORY:"):
        return False, ("CAT_FIELD_ERROR", "Field 4 must start with 'CATEGORY:'", raw_line)
    cat_val = t_cat.strip()[9:].upper()
    valid_categories = ["GENERAL", "OBC", "SC", "ST", "EWS"]
    if cat_val not in valid_categories:
        return False, ("CATEGORY_ENUM_ERROR", f"Unknown category '{cat_val}'. Allowed: {valid_categories}", raw_line)
        
    # 5. Status token validation
    if not t_stat.strip().startswith("STATUS:"):
        return False, ("STATUS_FIELD_ERROR", "Field 5 must start with 'STATUS:'", raw_line)
    stat_val = t_stat.strip()[7:].upper()
    valid_statuses = ["CONFIRMED", "PROVISIONAL", "WAITLISTED"]
    if stat_val not in valid_statuses:
        return False, ("STATUS_ENUM_ERROR", f"Unknown status '{stat_val}'. Allowed: {valid_statuses}", raw_line)
        
    full_reg_id = f"REG#{year}-{dept}-{seq}"
    parsed_record = (full_reg_id, year, dept, seq, clean_name, dob_val, cat_val, stat_val)
    return True, parsed_record


def process_registration_batch(raw_records):
    """
    Processes a batch of raw registration strings,
    extracts valid tuples, checks duplicate IDs, and categorizes errors.
    """
    valid_parsed_records = []
    registered_ids = []
    error_records = []
    
    for idx in range(len(raw_records)):
        line = raw_records[idx]
        rec_num = idx + 1
        is_valid, result = analyze_raw_registration_string(line)
        
        if is_valid:
            reg_id, year, dept, seq, name, dob, cat, stat = result
            # Check for duplicate registration keys
            if reg_id in registered_ids:
                error_records.append((rec_num, "DUPLICATE_KEY_ERROR", f"Duplicate registration identifier '{reg_id}' detected.", line))
            else:
                registered_ids.append(reg_id)
                valid_parsed_records.append(result)
        else:
            err_type, err_desc, orig_str = result
            error_records.append((rec_num, err_type, err_desc, orig_str))
            
    return valid_parsed_records, error_records


def display_registration_audit(valid_records, error_records):
    """Prints a formatted report of parsed structured records and error classifications."""
    border = "=" * 98
    dash = "-" * 98
    
    print("\n" + border)
    print(" " * 24 + "DR. RVR NRI INSTITUTE OF TECHNOLOGY")
    print(" " * 22 + "CAMPUS ADMISSION REGISTRATION STRING ANALYZER")
    print(border)
    print(f"Total Strings Processed: {len(valid_records) + len(error_records)}")
    print(f"Successfully Extracted : {len(valid_records)}")
    print(f"Rejected / Malformed   : {len(error_records)}")
    print(dash)
    
    print("PARSED STRUCTURED REGISTRATION DATABASE:")
    print(f"{'Reg ID':<19}{'Dept':<6}{'Year':<6}{'Candidate Name':<22}{'DOB':<12}{'Category':<10}{'Status':<12}")
    print(dash)
    for rec in valid_records:
        rid, yr, dept, seq, name, dob, cat, stat = rec
        print(f"{rid:<19}{dept:<6}{yr:<6}{name:<22}{dob:<12}{cat:<10}{stat:<12}")
        
    print(dash)
    
    if len(error_records) > 0:
        print("[!] PARSING DEFECT CLASSIFICATION & AUDIT LOG:")
        for err in error_records:
            rnum, etype, edesc, raw = err
            print(f"    - Entry #{rnum} | Defect Class: {etype:<20}")
            print(f"      Reason: {edesc}")
            print(f"      Raw   : \"{raw}\"")
    else:
        print("[*] All input registration strings conformed perfectly to specification.")
    print(border + "\n")


def run_demo():
    """Demonstration dataset featuring valid records, delimiter errors, bad dates, and duplicates."""
    raw_inputs = [
        # 1. Perfectly formatted valid record
        "REG#2026-CSE-0142|NAME:Aditya_Sharma|DOB:2006-05-14|CATEGORY:GENERAL|STATUS:CONFIRMED",
        
        # 2. Valid record for ECE
        "REG#2026-ECE-0205|NAME:Bhavya_Sri_Reddy|DOB:2005-11-20|CATEGORY:OBC|STATUS:PROVISIONAL",
        
        # 3. Delimiter Error (only 3 fields, missing status and category)
        "REG#2026-CSE-0143|NAME:Charan_Teja|DOB:2006-02-10",
        
        # 4. Invalid Department code in Reg Token ('BIOTECH' is not in allowed departments)
        "REG#2026-BIO-0999|NAME:Divya_Rao|DOB:2005-08-15|CATEGORY:SC|STATUS:CONFIRMED",
        
        # 5. Invalid DOB (Month 14 out of range)
        "REG#2026-INF-0410|NAME:Eshwar_Prasad|DOB:2006-14-05|CATEGORY:ST|STATUS:CONFIRMED",
        
        # 6. Duplicate Key Error (Repeat of REG#2026-CSE-0142)
        "REG#2026-CSE-0142|NAME:Another_Student|DOB:2006-01-01|CATEGORY:GENERAL|STATUS:WAITLISTED",
        
        # 7. Another valid record
        "REG#2026-MEC-0315|NAME:Fatima_Zahra|DOB:2006-09-30|CATEGORY:EWS|STATUS:CONFIRMED"
    ]
    
    valid, errors = process_registration_batch(raw_inputs)
    display_registration_audit(valid, errors)


if __name__ == "__main__":
    run_demo()
