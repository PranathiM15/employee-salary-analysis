# Aurora Salary Lab — Employee Salary Analysis

**VEDA TECHNOLOGY · Task 3 · AI & ML Track**

A terminal-first Python project and browser dashboard for manually entering and analyzing employee salary data.

## What the task asks for

The supplied Task 3 instructions require a Python program that analyzes employee salaries and calculates:

- Total salary
- Average salary
- Highest salary
- Lowest salary

The suggested dataset is **manually created employee salary data**.

## How this version works

You can now enter employee data **manually inside the web application**.

Fill in:

1. Employee ID
2. Employee name
3. Role
4. Department
5. Salary

Click **Add Employee**.

The Python backend automatically saves the record to `data/salaries.json` and recalculates the:

- Total salary
- Average salary
- Highest salary
- Lowest salary
- Employee count

You can also remove individual records, clear the whole dataset, search the table, or load the example dataset.

## Tools used

- Python
- Python standard library (`http.server`, `json`, `pathlib`)
- HTML
- CSS
- JavaScript
- No Jupyter Notebook required
- No pandas required
- No external Python packages required

## Run in Terminal

Open PowerShell in the project folder:

```powershell
cd "D:\veda technology\employee-salary-analysis"
py app.py
```

Then open:

```text
http://127.0.0.1:8000
```

Stop the server with:

```text
Ctrl + C
```

## Optional terminal-only calculation

You can also run the analysis program directly:

```powershell
py salary_analysis.py
```

It reads the current `data/salaries.json` dataset and prints the salary statistics.

## Project structure

```text
employee-salary-analysis/
│
├── app.py
├── salary_analysis.py
├── README.md
├── requirements.txt
├── RUN_IN_TERMINAL.txt
├── TASK_NOTES.md
│
├── data/
│   └── salaries.json
│
└── static/
    ├── index.html
    ├── style.css
    └── app.js
```

## Interview questions

### How do you calculate the average salary?

```python
average = sum(salaries) / len(salaries)
```

The total of all salaries is divided by the number of employees.

### Difference between total salary and average salary

Total salary is the combined value of all employee salaries. Average salary is the total divided by the number of employees.

### How would you analyze salary data using Pandas?

A Pandas DataFrame can store employee records, and `.sum()`, `.mean()`, `.max()` and `.min()` can calculate the same statistics. This project uses Python built-in functions instead, so it can run directly from Terminal without installing Pandas or Jupyter.

## Submission checklist

- [x] Python salary analysis
- [x] Manually created salary dataset
- [x] Manual employee data entry in the web app
- [x] Total, average, highest and lowest calculations
- [x] Short README
- [x] Unique web dashboard
- [ ] Push the project to a public GitHub repository
- [ ] Share the completed project on LinkedIn
- [ ] Submit the repository link through the Veda Technology internship portal

## GitHub repository

Suggested repository name:

`employee-salary-analysis`

Create the GitHub repository as **Public** and keep it empty (do not add another README, `.gitignore`, or license) before pushing this local project.

Git commands:

```powershell
git init -b main
git add .
git status
git commit -m "Complete Task 3 employee salary analysis"
git remote add origin https://github.com/PranathiM15/employee-salary-analysis.git
git remote -v
git push -u origin main
```
