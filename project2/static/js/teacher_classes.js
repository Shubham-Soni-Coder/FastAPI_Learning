// Teacher Classes - Mock Data & Logic

// Mock Data
const classesData = [
  {
    id: 1,
    name: "Grade 10-A",
    subject: "Mathematics",
    students: 32,
    time: "09:00 AM - 10:30 AM",
    color: "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
  },
  {
    id: 2,
    name: "Grade 9-B",
    subject: "Physics",
    students: 28,
    time: "11:30 AM - 01:00 PM",
    color: "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
  },
  {
    id: 3,
    name: "Grade 10-C",
    subject: "Geometry",
    students: 30,
    time: "02:00 PM - 03:30 PM",
    color: "linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)",
  },
  {
    id: 4,
    name: "Grade 8-A",
    subject: "Basic Algebra",
    students: 25,
    time: "10:00 AM - 11:30 AM",
    color: "linear-gradient(135deg, #cfd9df 0%, #e2ebf0 100%)",
  },
];

document.addEventListener("DOMContentLoaded", () => {
  const cardViewBtn = document.getElementById("cardViewBtn");
  const tableViewBtn = document.getElementById("tableViewBtn");
  const classesContainer = document.getElementById("classesContainer");
  const classesTableContainer = document.getElementById(
    "classesTableContainer"
  );
  const classesTableBody = document.getElementById("classesTableBody");

  // Render Functions
  function renderCards() {
    classesContainer.innerHTML = classesData
      .map(
        (cls) => `
            <div class="class-card">
                <div class="class-header-bg" style="background: ${cls.color}">
                    <span class="class-badge">${cls.name}</span>
                </div>
                <div class="class-body">
                    <h3 class="class-title">${cls.subject}</h3>
                    <div class="class-stats">
                        <div class="stat-item">
                            <i class="fa-solid fa-user-group"></i>
                            <span>${cls.students} Students</span>
                        </div>
                        <div class="stat-item">
                            <i class="fa-solid fa-clock"></i>
                            <span>${cls.time.split(" - ")[0]}</span>
                        </div>
                    </div>
                    <div class="card-footer">
                        <button class="open-class-btn" onclick="openClass('${cls.name}')">
                            Open Class <i class="fa-solid fa-arrow-right"></i>
                        </button>
                    </div>
                </div>
            </div>
        `
      )
      .join("");
  }

  function renderTable() {
    classesTableBody.innerHTML = classesData
      .map(
        (cls) => `
            <tr>
                <td style="font-weight: 500;">${cls.name}</td>
                <td>${cls.subject}</td>
                <td>${cls.students}</td>
                <td>${cls.time}</td>
                <td>
                    <button class="table-action-btn" onclick="openClass('${cls.name}')">
                        Open Class
                    </button>
                </td>
            </tr>
        `
      )
      .join("");
  }

  // View Toggles
  cardViewBtn.addEventListener("click", () => {
    cardViewBtn.classList.add("active");
    tableViewBtn.classList.remove("active");
    classesContainer.classList.remove("hidden");
    classesTableContainer.classList.add("hidden");
  });

  tableViewBtn.addEventListener("click", () => {
    tableViewBtn.classList.add("active");
    cardViewBtn.classList.remove("active");
    classesTableContainer.classList.remove("hidden");
    classesContainer.classList.add("hidden");
  });

  // Initial Render
  renderCards();
  renderTable();
});

// Global function for onclick (CTA)
window.openClass = function (className) {
  alert(`Opening class: ${className}`);
  // In a real app, this would navigate to the detailed class view
  // window.location.href = `/teacher/class/${className}`;
};
