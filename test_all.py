"""
Root Test Suite: Execute and Verify All 10 Activity-Based Learning Case Studies
"""
import os
import subprocess
import sys

CASE_STUDIES = [
    ("Case Study 02: Progressive Electricity Billing", "Case_Study_02_Electricity_Billing/solution.py"),
    ("Case Study 26: Seating Arrangement Generator", "Case_Study_26_Seating_Arrangement/solution.py"),
    ("Case Study 27: Numeric Pattern Generator", "Case_Study_27_Pattern_Generator/solution.py"),
    ("Case Study 31: Answer Key Evaluator", "Case_Study_31_Answer_Key_Evaluator/solution.py"),
    ("Case Study 42: Marks Matrix Analysis", "Case_Study_42_Marks_Matrix_Analysis/solution.py"),
    ("Case Study 48: Shift Conflict Detector", "Case_Study_48_Shift_Conflict_Detector/solution.py"),
    ("Case Study 56: Score Balancing Groups", "Case_Study_56_Score_Balancing_Groups/solution.py"),
    ("Case Study 75: Record Consistency Checker", "Case_Study_75_Record_Consistency_Checker/solution.py"),
    ("Case Study 91: Registration Analyzer", "Case_Study_91_Registration_Analyzer/solution.py"),
    ("Case Study 100: Campus Management Simulation", "Case_Study_100_Campus_Management_Simulation/solution.py")
]

def main():
    print("=" * 80)
    print("  DR. RVR NRI INSTITUTE OF TECHNOLOGY - ABL ASSIGNMENT TEST SUITE")
    print("=" * 80)
    
    passed_count = 0
    total = len(CASE_STUDIES)
    
    for title, script_path in CASE_STUDIES:
        full_path = os.path.normpath(script_path)
        print(f"\n[RUNNING] {title} ({full_path})...")
        
        result = subprocess.run([sys.executable, full_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"  --> PASSED (Exit Code 0)")
            passed_count += 1
        else:
            print(f"  --> FAILED (Exit Code {result.returncode})")
            print("  STDERR:")
            print(result.stderr)
            
    print("\n" + "=" * 80)
    print(f"  SUMMARY: {passed_count}/{total} CASE STUDIES PASSED SUCCESSFULLY")
    print("=" * 80)
    
    if passed_count == total:
        print("[SUCCESS] All 10 case study programs execute without errors!")
        sys.exit(0)
    else:
        print("[ERROR] Some case studies failed. Please review.")
        sys.exit(1)

if __name__ == "__main__":
    main()
