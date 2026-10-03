from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import json

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "salaries.json"
STATIC_DIR = ROOT / "static"
HOST = "127.0.0.1"
PORT = 8000


def load_employees():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file).get("employees", [])


def save_employees(employees):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump({"employees": employees}, file, indent=2, ensure_ascii=False)


def analyze(employees):
    salaries = [float(employee["salary"]) for employee in employees]

    if not salaries:
        return {
            "total": 0,
            "average": 0,
            "highest": 0,
            "lowest": 0,
            "highest_employee": None,
            "lowest_employee": None,
            "count": 0,
        }

    highest_employee = max(employees, key=lambda item: float(item["salary"]))
    lowest_employee = min(employees, key=lambda item: float(item["salary"]))

    return {
        "total": sum(salaries),
        "average": sum(salaries) / len(salaries),
        "highest": max(salaries),
        "lowest": min(salaries),
        "highest_employee": highest_employee,
        "lowest_employee": lowest_employee,
        "count": len(salaries),
    }


class SalaryHandler(BaseHTTPRequestHandler):
    def send_json(self, payload, status=200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path, content_type):
        try:
            body = path.read_bytes()
        except FileNotFoundError:
            self.send_error(404, "File not found")
            return

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json_body(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        route = urlparse(self.path).path

        if route == "/":
            self.send_file(STATIC_DIR / "index.html", "text/html; charset=utf-8")
        elif route == "/api/data":
            employees = load_employees()
            self.send_json({"employees": employees, "analysis": analyze(employees)})
        elif route == "/api/health":
            self.send_json({"status": "ok"})
        elif route == "/style.css":
            self.send_file(STATIC_DIR / "style.css", "text/css; charset=utf-8")
        elif route == "/app.js":
            self.send_file(STATIC_DIR / "app.js", "application/javascript; charset=utf-8")
        else:
            self.send_error(404, "Route not found")

    def do_POST(self):
        route = urlparse(self.path).path

        try:
            payload = self.read_json_body()

            if route == "/api/employees":
                action = payload.get("action")

                if action == "replace":
                    employees = payload.get("employees", [])
                    cleaned = validate_employees(employees)
                    save_employees(cleaned)
                    self.send_json({"message": "Dataset saved.", "employees": cleaned, "analysis": analyze(cleaned)})
                    return

                if action == "add":
                    employee = validate_employee(payload.get("employee", {}))
                    employees = load_employees()
                    employees.append(employee)
                    save_employees(employees)
                    self.send_json({"message": "Employee added.", "employees": employees, "analysis": analyze(employees)})
                    return

                if action == "delete":
                    employee_id = str(payload.get("id", "")).strip()
                    employees = [item for item in load_employees() if item["id"] != employee_id]
                    save_employees(employees)
                    self.send_json({"message": "Employee deleted.", "employees": employees, "analysis": analyze(employees)})
                    return

                if action == "clear":
                    save_employees([])
                    self.send_json({"message": "Dataset cleared.", "employees": [], "analysis": analyze([])})
                    return

                self.send_json({"error": "Unknown employee action."}, 400)
                return

            self.send_json({"error": "Route not found."}, 404)

        except (ValueError, TypeError, json.JSONDecodeError) as error:
            self.send_json({"error": str(error)}, 400)


def validate_employee(employee):
    if not isinstance(employee, dict):
        raise ValueError("Employee data must be an object.")

    employee_id = str(employee.get("id", "")).strip()
    name = str(employee.get("name", "")).strip()
    role = str(employee.get("role", "")).strip()
    department = str(employee.get("department", "")).strip()

    if not all([employee_id, name, role, department]):
        raise ValueError("ID, name, role and department are required.")

    try:
        salary = float(employee.get("salary"))
    except (TypeError, ValueError):
        raise ValueError("Salary must be a valid number.")

    if salary <= 0:
        raise ValueError("Salary must be greater than 0.")

    return {
        "id": employee_id,
        "name": name,
        "role": role,
        "department": department,
        "salary": salary,
    }


def validate_employees(employees):
    if not isinstance(employees, list):
        raise ValueError("Employees must be a list.")
    return [validate_employee(employee) for employee in employees]


if __name__ == "__main__":
    print("=" * 62)
    print("EMPLOYEE SALARY ANALYSIS • AURORA SALARY LAB")
    print("=" * 62)
    print(f"Open: http://{HOST}:{PORT}")
    print("Add employee salary data directly from the web app.")
    print("Press Ctrl+C to stop the server.")
    print("=" * 62)
    ThreadingHTTPServer((HOST, PORT), SalaryHandler).serve_forever()
