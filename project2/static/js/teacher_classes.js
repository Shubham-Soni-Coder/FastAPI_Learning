// Teacher Classes - Dynamic Data & Logic

let classesData = [];
// Colors to cycle through for cards
const classColors = [
  "#8c7ae6", // Purple
  "#ff7675", // Salmon
  "#00b894", // Teal
  "#74b9ff", // Blue
  "#e67e22", // Orange
  "#fd79a8", // Pink
  "#fbc531", // Yellow
  "#2d3436"  // Dark Grey
];

document.addEventListener("DOMContentLoaded", () => {
  const cardViewBtn = document.getElementById("cardViewBtn");
  const tableViewBtn = document.getElementById("tableViewBtn");
  const classesContainer = document.getElementById("classesContainer");
  const classesTableContainer = document.getElementById("classesTableContainer");
  const classesTableBody = document.getElementById("classesTableBody");

  // Fetch Data from Backend
  async function fetchClasses() {
    try {
      const response = await fetch('/teacher/api/classes-list');
      if (!response.ok) throw new Error('Failed to fetch classes');

      const data = await response.json();

      // Enhance data with colors
      classesData = data.map((cls, index) => ({
        ...cls,
        color: classColors[index % classColors.length]
      }));

      renderCards();
      renderTable();

    } catch (error) {
      console.error("Error loading classes:", error);
      if (classesContainer) {
        classesContainer.innerHTML = `<p class="error-msg">Failed to load classes. Please try again.</p>`;
      }
    }
  }

  // Render Functions
  function renderCards() {
    if (!classesContainer) return;

    if (classesData.length === 0) {
      classesContainer.innerHTML = '<p class="empty-msg">No classes found.</p>';
      return;
    }

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
                        <button class="action-btn btn-primary" onclick="openClass(${cls.id})">Start Class</button>
                        <button class="action-btn btn-outline" onclick="openAttendance(${cls.id})">Attendance</button>
                    </div>
                </div>
            </div>
        `
      )
      .join("");
  }

  function renderTable() {
    if (!classesTableBody) return;

    classesTableBody.innerHTML = classesData
      .map(
        (cls) => `
            <tr>
                <td style="font-weight: 500;">${cls.name}</td>
                <td>${cls.subject}</td>
                <td>${cls.students}</td>
                <td>${cls.time}</td>
                <td>
                    <button class="table-action-btn" onclick="openClass(${cls.id})">
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

  // Initial Fetch
  fetchClasses();
});

// Global navigation functions
window.openClass = function (batchId) {
  // Can link to a specific "Start Class" view or just the details
  window.location.href = `/teacher/classes/details?batch_id=${batchId}&mode=start`;
};

window.openAttendance = function (batchId) {
  // Link to the attendance tab of the details page
  window.location.href = `/teacher/classes/details?batch_id=${batchId}&tab=attendance`;
};
