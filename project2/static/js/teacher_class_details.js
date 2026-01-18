// Teacher Class Details - Attendance Logic


document.addEventListener('DOMContentLoaded', () => {
    // Set Date to Today
    document.getElementById('attendanceDate').valueAsDate = new Date();

    const attendanceGrid = document.getElementById('attendanceGrid');
    const presentCountEl = document.getElementById('presentCount');
    const absentCountEl = document.getElementById('absentCount');
    const markAllPresentBtn = document.getElementById('markAllPresentBtn');
    const saveAttendanceBtn = document.getElementById('saveAttendanceBtn');

    // Use global studentsData
    let studentsData = window.studentsData || [];

    // Render Student Cards
    function renderStudents() {
        if (!studentsData.length) {
            attendanceGrid.innerHTML = '<p style="text-align:center; width:100%; color: var(--text-muted);">No students found.</p>';
            return;
        }

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
            if (btn) {
                btn.className = `attendance-toggle ${student.status}`;
                btn.innerHTML = `<i class="fa-solid ${student.status === 'present' ? 'fa-check' : 'fa-xmark'}"></i>`;
            }

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
        // Collect data to send
        const attendancePayload = studentsData.map(s => ({
            student_id: s.id,
            status: s.status,
            date: document.getElementById('attendanceDate').value
        }));

        console.log('Saving attendance:', attendancePayload);
        alert('Attendance Saved Successfully for ' + document.getElementById('attendanceDate').value);

        // Example POST request (commented out until backend endpoint is ready)
        /*
        fetch('/teacher/attendance/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(attendancePayload)
        });
        */
    });

    // Initial Render
    renderStudents();
});
