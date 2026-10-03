"""
Employee Salary Analysis
Terminal version of Task 3.

Uses only Python's standard library.
No Jupyter Notebook, pandas, or external packages are required.
"""

from pathlib import Path
import json

DATA_FILE = Path(__file__).resolve().parent / "data" / "salaries.json"


def load_data():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)["employees"]


def main():
    employees = load_data()
    salaries = [employee["salary"] for employee in employees]

    total = sum(salaries)
    average = total / len(salaries)
    highest = max(salaries)
    lowest = min(salaries)

    highest_employee = max(employees, key=lambda employee: employee["salary"])
    lowest_employee = min(employees, key=lambda employee: employee["salary"])

    print("\nEMPLOYEE SALARY ANALYSIS")
    print("-" * 42)
    print(f"Employees       : {len(salaries)}")
    print(f"Total salary    : ₹{total:,.0f}")
    print(f"Average salary  : ₹{average:,.2f}")
    print(f"Highest salary  : ₹{highest:,.0f} ({highest_employee['name']})")
    print(f"Lowest salary   : ₹{lowest:,.0f} ({lowest_employee['name']})")
    print("-" * 42)

    print("\nOriginal salary data:")
    for employee in employees:
        print(f"  {employee['id']} | {employee['name']:<18} | {employee['role']:<18} | ₹{employee['salary']:,.0f}")

    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()
