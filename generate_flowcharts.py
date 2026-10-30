"""Make simple flowcharts for the case study programs."""

import html
import os


FLOWCHARTS = {
    "Case_Study_02_Electricity_Billing": (
        "Case 02: Electricity Bill",
        ["Start", "Read monthly units", "Calculate charge from unit slabs",
         "Add fixed charge", "Apply surcharge or rebate", "Compare with last month",
         "Save and print bill", "End"],
    ),
    "Case_Study_26_Seating_Arrangement": (
        "Case 26: Exam Seating Plan",
        ["Start", "Make a grid of vacant seats", "Mark reserved seats",
         "Check each seat", "Check nearby departments", "Seat a student or mark a buffer",
         "Print the seating plan", "End"],
    ),
    "Case_Study_27_Pattern_Generator": (
        "Case 27: Number Patterns",
        ["Start", "Check the pattern size", "Find the middle row",
         "Print the top half", "Print the middle row", "Print the bottom half",
         "Print the second pattern", "End"],
    ),
    "Case_Study_31_Answer_Key_Evaluator": (
        "Case 31: Answer Key",
        ["Start", "Check answer format", "Check each question",
         "Compare answers with the key", "Calculate scores", "Sort the results",
         "Print the results", "End"],
    ),
    "Case_Study_42_Marks_Matrix_Analysis": (
        "Case 42: Marks Analysis",
        ["Start", "Check each student's marks", "Find totals and grades",
         "Check each subject", "Find subject results", "Mark subjects needing help",
         "Print the results", "End"],
    ),
    "Case_Study_48_Shift_Conflict_Detector": (
        "Case 48: Shift Checker",
        ["Start", "Convert times to minutes", "Check each shift",
         "Compare shifts two at a time", "Check for overlaps", "Check rest time",
         "Print any problems", "End"],
    ),
    "Case_Study_56_Score_Balancing_Groups": (
        "Case 56: Student Groups",
        ["Start", "Sort students by score", "Make empty groups",
         "Add students from first group to last", "Add students back in reverse",
         "Compare group totals", "Print the groups", "End"],
    ),
    "Case_Study_75_Record_Consistency_Checker": (
        "Case 75: Student Record Checker",
        ["Start", "Check each student record", "Check roll number and name",
         "Check marks and attendance", "Keep valid records", "Note record problems",
         "Print the results", "End"],
    ),
    "Case_Study_91_Registration_Analyzer": (
        "Case 91: Registration Checker",
        ["Start", "Split the line into fields", "Check registration number",
         "Check name and date", "Check category and status",
         "Look for duplicate numbers", "Print records and problems", "End"],
    ),
    "Case_Study_100_Campus_Management_Simulation": (
        "Case 100: Campus Management",
        ["Start", "Make sample campus data", "Calculate marks and eligibility",
         "Register students for events", "Check room bookings",
         "Collect the results", "Print campus information", "End"],
    ),
}


def make_svg(title, steps):
    """Return a simple top-to-bottom diagram as SVG text."""
    width = 700
    box_width = 480
    box_height = 44
    gap = 22
    first_y = 78
    height = first_y + len(steps) * (box_height + gap)
    center_x = width / 2
    left_x = (width - box_width) / 2

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="100%" height="{height}" style="font-family: Arial, sans-serif;">',
        "<defs>",
        '<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto">',
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="#333" />',
        "</marker>",
        "</defs>",
        f'<text x="{center_x}" y="38" text-anchor="middle" font-size="19" '
        f'font-weight="bold" fill="#222">{html.escape(title)}</text>',
    ]

    for index, step in enumerate(steps):
        y = first_y + index * (box_height + gap)
        if index < len(steps) - 1:
            svg.append(
                f'<line x1="{center_x}" y1="{y + box_height}" '
                f'x2="{center_x}" y2="{y + box_height + gap - 3}" '
                'stroke="#333" stroke-width="1.5" marker-end="url(#arrow)" />'
            )

        if index == 0 or index == len(steps) - 1:
            fill = "#e2f0d9"
        else:
            fill = "#e8f0fe"
        svg.append(
            f'<rect x="{left_x}" y="{y}" width="{box_width}" height="{box_height}" '
            f'rx="5" fill="{fill}" stroke="#333" stroke-width="1.2" />'
        )
        svg.append(
            f'<text x="{center_x}" y="{y + 27}" text-anchor="middle" '
            f'font-size="14" fill="#222">{html.escape(step)}</text>'
        )

    svg.append("</svg>")
    return "\n".join(svg)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for folder, (title, steps) in FLOWCHARTS.items():
        target_path = os.path.join(base_dir, folder, "flowchart.svg")
        with open(target_path, "w", encoding="utf-8") as file:
            file.write(make_svg(title, steps))
        print(f"Made {folder}\\flowchart.svg")


if __name__ == "__main__":
    main()
