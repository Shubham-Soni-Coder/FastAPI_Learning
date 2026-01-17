// Teacher Classes - Mock Data & Logic

// Mock Data matching the reference image colors
const classesData = [
  {
    id: 1,
    name: "Grade 10-A",
    subject: "Mathematics",
    students: 32,
    time: "09:00 AM",
    // Purple like the first card
    color: "#8c7ae6",
  },
  {
    id: 2,
    name: "Grade 9-B",
    subject: "Physics",
    students: 28,
    time: "11:30 AM",
    // Salmon/Red like the second card
    color: "#ff7675",
  },
  {
    id: 3,
    name: "Grade 10-C",
    subject: "Geometry",
    students: 30,
    time: "02:00 PM",
    // Teal/Green like the third card
    color: "#00b894",
  },
  {
    id: 4,
    name: "Grade 8-A",
    subject: "Basic Algebra",
    students: 25,
    time: "10:00 AM",
    // Grey or Blue variant
    color: "#74b9ff",
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
                <!-- Top Half: Solid Color -->
                <div class="class-header-color" style="background: ${cls.color}">
                    <span class="class-badge">${cls.name}</span>
                </div>
                
                <!-- Bottom Half: Dark Glass -->
                <div class="class-body-glass">
                    <h3 class="class-title">${cls.subject}</h3>
                    
                    <div class="class-meta-row">
                        <span><i class="fa-solid fa-clock"></i> ${cls.time}</span>
                        <span><i class="fa-solid fa-user-group"></i> ${cls.students} Students</span>
                    </div>
                    
                    <div class="class-actions-row">
                        <button class="action-btn btn-primary" onclick="openClass('${cls.name}')">Start Class</button>
                        <button class="action-btn btn-outline" onclick="openAttendance('${cls.name}')">Attendance</button>
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
  if (cardViewBtn && tableViewBtn) {
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
  }

  // Initial Render
  if (classesContainer) renderCards();
  if (classesTableBody) renderTable();
});

// Global navigation functions
window.openClass = function (className) {
  // Can link to a specific "Start Class" view or just the details
  window.location.href = `/teacher/classes/details?className=${encodeURIComponent(className)}&mode=start`;
};

window.openAttendance = function (className) {
  // Link to the attendance tab of the details page
  window.location.href = `/teacher/classes/details?className=${encodeURIComponent(className)}&tab=attendance`;
};
