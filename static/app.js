const money = value =>
  new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0
  }).format(value);

let employees = [];
let allEmployeesBeforeSearch = [];

async function api(payload) {
  const response = await fetch("/api/employees", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Something went wrong.");
  return data;
}

function showMessage(text, error = false) {
  const box = document.getElementById("message");
  box.textContent = text;
  box.style.color = error ? "#ffb2b2" : "";
}

function renderStats(analysis) {
  document.getElementById("employeeCount").textContent = analysis.count;
  document.getElementById("total").textContent = money(analysis.total);
  document.getElementById("average").textContent = money(analysis.average);
  document.getElementById("highest").textContent = money(analysis.highest);
  document.getElementById("lowest").textContent = money(analysis.lowest);

  document.getElementById("highestPerson").textContent =
    analysis.highest_employee
      ? `${analysis.highest_employee.name} · ${money(analysis.highest)}`
      : "—";
  document.getElementById("lowestPerson").textContent =
    analysis.lowest_employee
      ? `${analysis.lowest_employee.name} · ${money(analysis.lowest)}`
      : "—";
}

function renderChart() {
  const chart = document.getElementById("salaryChart");

  if (!employees.length) {
    chart.innerHTML = '<div class="empty-state">Add employee data to generate the salary chart.</div>';
    return;
  }

  const maxSalary = Math.max(...employees.map(e => Number(e.salary)));

  chart.innerHTML = employees
    .slice()
    .sort((a, b) => Number(b.salary) - Number(a.salary))
    .map(employee => {
      const width = (Number(employee.salary) / maxSalary) * 100;
      return `
        <div class="bar-row">
          <div class="bar-name">${escapeHtml(employee.name)}</div>
          <div class="bar-track">
            <div class="bar-fill" style="width:${width}%"></div>
          </div>
          <div class="bar-value">${money(employee.salary)}</div>
        </div>
      `;
    }).join("");
}

function renderTable(list = employees) {
  const tbody = document.getElementById("employeeTable");

  if (!list.length) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" style="text-align:center;color:var(--muted);padding:28px">
          No employee records yet. Add your first employee above.
        </td>
      </tr>`;
    return;
  }

  tbody.innerHTML = list.map(employee => `
    <tr>
      <td>${escapeHtml(employee.id)}</td>
      <td>${escapeHtml(employee.name)}</td>
      <td>${escapeHtml(employee.role)}</td>
      <td>${escapeHtml(employee.department)}</td>
      <td>${money(employee.salary)}</td>
      <td><button class="remove-button" data-id="${escapeHtml(employee.id)}">Remove</button></td>
    </tr>
  `).join("");

  tbody.querySelectorAll(".remove-button").forEach(button => {
    button.addEventListener("click", () => removeEmployee(button.dataset.id));
  });
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function refresh(payload) {
  employees = payload.employees || [];
  allEmployeesBeforeSearch = [...employees];
  renderStats(payload.analysis);
  renderChart();
  renderTable();
}

async function loadDashboard() {
  try {
    const response = await fetch("/api/data");
    const payload = await response.json();
    refresh(payload);
  } catch (error) {
    showMessage("Could not load the Python data. Make sure py app.py is running.", true);
  }
}

document.getElementById("employeeForm").addEventListener("submit", async event => {
  event.preventDefault();

  const form = new FormData(event.target);
  const employee = {
    id: form.get("id").trim(),
    name: form.get("name").trim(),
    role: form.get("role").trim(),
    department: form.get("department").trim(),
    salary: Number(form.get("salary"))
  };

  try {
    const payload = await api({ action: "add", employee });
    refresh(payload);
    event.target.reset();
    document.getElementById("id").focus();
    showMessage(`${employee.name} added successfully. Statistics updated.`);
  } catch (error) {
    showMessage(error.message, true);
  }
});

async function removeEmployee(id) {
  try {
    const payload = await api({ action: "delete", id });
    refresh(payload);
    showMessage("Employee removed and statistics updated.");
  } catch (error) {
    showMessage(error.message, true);
  }
}

document.getElementById("clearAll").addEventListener("click", async () => {
  if (!employees.length) {
    showMessage("There are no records to clear.");
    return;
  }

  const confirmed = confirm("Clear every employee record from the dataset?");
  if (!confirmed) return;

  try {
    const payload = await api({ action: "clear" });
    refresh(payload);
    showMessage("Dataset cleared. You can now enter your own employee data.");
  } catch (error) {
    showMessage(error.message, true);
  }
});

document.getElementById("loadSample").addEventListener("click", async () => {
  const sample = [
    {"id":"EMP001","name":"Aarav Mehta","role":"Software Engineer","department":"Engineering","salary":72000},
    {"id":"EMP002","name":"Diya Rao","role":"Data Analyst","department":"Analytics","salary":68000},
    {"id":"EMP003","name":"Kabir Shah","role":"Product Designer","department":"Design","salary":61000},
    {"id":"EMP004","name":"Anaya Iyer","role":"ML Engineer","department":"AI & ML","salary":94000},
    {"id":"EMP005","name":"Rohan Nair","role":"Backend Developer","department":"Engineering","salary":83000},
    {"id":"EMP006","name":"Ishita Menon","role":"HR Executive","department":"People","salary":54000},
    {"id":"EMP007","name":"Vivaan Kapoor","role":"Cloud Engineer","department":"Infrastructure","salary":89000},
    {"id":"EMP008","name":"Meera Joshi","role":"QA Engineer","department":"Quality","salary":65000},
    {"id":"EMP009","name":"Arjun Rao","role":"Frontend Developer","department":"Engineering","salary":76000},
    {"id":"EMP010","name":"Sara Thomas","role":"Business Analyst","department":"Analytics","salary":70000}
  ];

  try {
    const payload = await api({ action: "replace", employees: sample });
    refresh(payload);
    showMessage("Example dataset loaded. You can remove it and enter your own records.");
  } catch (error) {
    showMessage(error.message, true);
  }
});

document.getElementById("search").addEventListener("input", event => {
  const query = event.target.value.toLowerCase().trim();

  const filtered = allEmployeesBeforeSearch.filter(employee =>
    [employee.id, employee.name, employee.role, employee.department]
      .some(value => value.toLowerCase().includes(query))
  );

  renderTable(filtered);
});

loadDashboard();
