// Teacher Class Details - Attendance Logic

// Mock Data for Students (Grade 10-A)
const maxStudents = 32;
const studentsData = Array.from({ length: maxStudents }, (_, i) => {
    const names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Martinez", "Lopez"];
    const firstNames = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth"];

    const randomFirst = firstNames[Math.floor(Math.random() * firstNames.length)];
    const randomLast = names[Math.floor(Math.random() * names.length)];

    return {
        id: i + 1,
        rollNo: 100 + i + 1,
        name: `${randomFirst} ${randomLast}`,
        initials: `${randomFirst[0]}${randomLast[0]}`,
        status: 'present' // default
    };
});

document.addEventListener('DOMContentLoaded', () => {
    // Set Date to Today
    document.getElementById('attendanceDate').valueAsDate = new Date();

    const attendanceGrid = document.getElementById('attendanceGrid');
    const presentCountEl = document.getElementById('presentCount');
    const absentCountEl = document.getElementById('absentCount');
    const markAllPresentBtn = document.getElementById('markAllPresentBtn');
    const saveAttendanceBtn = document.getElementById('saveAttendanceBtn');

    // Render Student Cards
    function renderStudents() {
        attendanceGrid.innerHTML = studentsData.map(student => `
            <div class="student-card" id="card-${student.id}">
                <div class="student-info">
                    <div class="student-avatar" style="background: hsl(${student.id * 15}, 70%, 50%)">
                        ${student.initials}
                    </div>
                    <div class="student-details">
                        <h4>${student.name}</h4>
                        <span class="student-roll">Roll No: #${student.rollNo}</span>
                    </div>
                </div>
                <button class="attendance-toggle ${student.status}" onclick="toggleAttendance(${student.id})">
                    <i class="fa-solid ${student.status === 'present' ? 'fa-check' : 'fa-xmark'}"></i>
                </button>
            </div>
        `).join('');
        updateStats();
    }

    // Update Counts
    function updateStats() {
        const present = studentsData.filter(s => s.status === 'present').length;
        const absent = studentsData.filter(s => s.status === 'absent').length;
        presentCountEl.textContent = present;
        absentCountEl.textContent = absent;
    }

    // Toggle Handler (Global scope)
    window.toggleAttendance = function (id) {
        const student = studentsData.find(s => s.id === id);
        if (student) {
            student.status = student.status === 'present' ? 'absent' : 'present';

            // Update UI for this specific card
            const btn = document.querySelector(`#card-${id} .attendance-toggle`);
            btn.className = `attendance-toggle ${student.status}`;
            btn.innerHTML = `<i class="fa-solid ${student.status === 'present' ? 'fa-check' : 'fa-xmark'}"></i>`;

            // Update stats
            updateStats();
        }
    };

    // Mark All Present
    markAllPresentBtn.addEventListener('click', () => {
        studentsData.forEach(s => s.status = 'present');
        renderStudents();
    });

    // Save Attendance
    saveAttendanceBtn.addEventListener('click', () => {
        alert('Attendance Saved Successfully for ' + document.getElementById('attendanceDate').value);
        // Here you would send a POST request to the backend
    });

    // Initial Render
    renderStudents();
});
