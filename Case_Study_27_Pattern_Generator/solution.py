"""Check a pattern size and print two number diamonds."""

def validate_pattern_dimension(n):
    """
    Validates that pattern dimension n is a positive odd integer
    within acceptable display limits (3 to 25).
    Returns (is_valid, error_message).
    """
    if not isinstance(n, int):
        return False, "Dimension must be an integer value."
    if n < 3:
        return False, "Dimension is too small; minimum size is 3."
    if n > 25:
        return False, "Dimension exceeds terminal display limit (maximum 25)."
    if n % 2 == 0:
        return False, f"Dimension {n} is even. A symmetric hollow diamond requires an ODD dimension."
    return True, "Dimension is valid."


def generate_hollow_numeric_diamond(n):
    """
    Generates a hollow diamond of numbers of height n (n must be odd).
    Outer borders display the current layer depth number with symmetric spacing.
    Returns list of pattern lines.
    """
    lines = []
    mid = n // 2  # 0 to mid is upper half, mid+1 to n-1 is lower half
    
    # 1. Upper Half (including center row)
    for i in range(mid + 1):
        outer_spaces = " " * (mid - i)
        num_char = str(i + 1)
        
        if i == 0:
            line = outer_spaces + num_char
        else:
            inner_spaces = " " * (2 * i - 1)
            line = outer_spaces + num_char + inner_spaces + num_char
            
        lines.append(line)
        
    # 2. Lower Half (symmetric reflection)
    for i in range(mid - 1, -1, -1):
        outer_spaces = " " * (mid - i)
        num_char = str(i + 1)
        
        if i == 0:
            line = outer_spaces + num_char
        else:
            inner_spaces = " " * (2 * i - 1)
            line = outer_spaces + num_char + inner_spaces + num_char
            
        lines.append(line)
        
    return lines


def generate_symmetric_palindromic_diamond(n):
    """
    Generates a full palindromic diamond where each row is a palindrome
    1 2 ... k ... 2 1 with proportional outer indentations.
    """
    lines = []
    mid = n // 2
    
    # Upper Half + Center
    for i in range(mid + 1):
        outer_spaces = "  " * (mid - i)
        # Ascending sequence
        row_nums = []
        for val in range(1, i + 2):
            row_nums.append(str(val))
        # Descending sequence
        for val in range(i, 0, -1):
            row_nums.append(str(val))
            
        line = outer_spaces + " ".join(row_nums)
        lines.append(line)
        
    # Lower Half
    for i in range(mid - 1, -1, -1):
        outer_spaces = "  " * (mid - i)
        row_nums = []
        for val in range(1, i + 2):
            row_nums.append(str(val))
        for val in range(i, 0, -1):
            row_nums.append(str(val))
            
        line = outer_spaces + " ".join(row_nums)
        lines.append(line)
        
    return lines


def display_pattern_suite(dimension):
    """Validates input, generates both patterns, and renders formatted output."""
    print("=" * 65)
    print("       ADVANCED NUMERIC & HOLLOW DIAMOND PATTERN SUITE       ")
    print("=" * 65)
    print(f"Target Dimension Request : N = {dimension}")
    
    is_valid, msg = validate_pattern_dimension(dimension)
    if not is_valid:
        print(f"[ERROR] Input Validation Failed: {msg}")
        print("=" * 65 + "\n")
        return
        
    print(f"[STATUS] Validation Passed: {msg}\n")
    
    print("--- Pattern 1: Symmetric Hollow Numeric Diamond ---")
    hollow_lines = generate_hollow_numeric_diamond(dimension)
    for line in hollow_lines:
        print(line)
        
    print("\n--- Pattern 2: Multi-Layer Palindromic Number Diamond ---")
    palindromic_lines = generate_symmetric_palindromic_diamond(dimension)
    for line in palindromic_lines:
        print(line)
        
    print("=" * 65 + "\n")


def run_demo():
    """Run test cases including invalid boundary tests and successful renders."""
    # Test 1: Even dimension rejection
    display_pattern_suite(6)
    
    # Test 2: Standard Odd dimension N = 7
    display_pattern_suite(7)
    
    # Test 3: Complex Odd dimension N = 9
    display_pattern_suite(9)


if __name__ == "__main__":
    run_demo()
