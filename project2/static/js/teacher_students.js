document.addEventListener('DOMContentLoaded', () => {
    // Initial Setup
    initProgressBars();
    initModalButtons();

    // Month Selector Logic
    const months = document.querySelectorAll('.month-item');
    const attendanceEl = document.querySelector('.Attendance');

    if (months.length && attendanceEl) {
        months.forEach(month => {
            month.addEventListener('click', async () => {
                // UI Update
                months.forEach(m => m.classList.remove('active'));
                month.classList.add('active');

                const selectedMonth = month.textContent.trim();
                attendanceEl.innerHTML = `Attendance (${selectedMonth})`;

                // Fetch Data
                try {
                    const response = await fetch(`/teacher/students/data?month=${selectedMonth}`);
                    if (!response.ok) throw new Error('Network response was not ok');
                    const students = await response.json();
                    renderTable(students);
                } catch (error) {
                    console.error('Error fetching data:', error);
                    // Optional: Show error to user
                }
            });
        });
    }

    // Modal Logic (Global)
    const viewModal = document.getElementById('viewModal');
    const editModal = document.getElementById('editModal');

    window.onclick = function (event) {
        if (event.target == viewModal) viewModal.style.display = "none";
        if (event.target == editModal) editModal.style.display = "none";
    }
});

function initProgressBars() {
    document.querySelectorAll('.progress-bar-fill[data-width]').forEach(bar => {
        bar.style.width = bar.dataset.width + '%';
    });
}

function initModalButtons() {
    const viewModal = document.getElementById('viewModal');
    const editModal = document.getElementById('editModal');

    // View Buttons
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.getElementById('viewName').textContent = btn.dataset.name;
            document.getElementById('viewRoll').textContent = 'Roll No: #' + btn.dataset.roll;
            document.getElementById('viewParent').textContent = btn.dataset.parent;
            document.getElementById('viewAttendance').textContent = btn.dataset.attendance + '%';
            document.getElementById('viewAvatar').textContent = btn.dataset.initials;
            viewModal.style.display = 'block';
        });
    });

    // Edit Buttons
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.getElementById('editName').value = btn.dataset.name;
            document.getElementById('editRoll').value = '#' + btn.dataset.roll;
            editModal.style.display = 'block';
        });
    });
}

function renderTable(students) {
    const tbody = document.getElementById('student-table-body');
    if (!tbody) return;

    tbody.innerHTML = ''; // Clear current rows

    students.forEach(student => {
        const tr = document.createElement('tr');

        const feesStatusHtml = student.fees_paid
            ? `<span class="status-badge paid">Paid</span>`
            : `<span class="status-badge pending">Pending</span>`;

        tr.innerHTML = `
            <td>#${student.roll_no}</td>
            <td>
                <div class="table-user-info">
                    <div class="table-avatar">${student.initials}</div>
                    <div>
                        <span style="font-weight: 600; display: block;">${student.name}</span>
                        <span style="font-size: 0.8rem; color: var(--text-muted);">${student.parent}</span>
                    </div>
                </div>
            </td>
            <td>${feesStatusHtml}</td>
            <td>
                <div class="progress-wrapper">
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" data-width="${student.attendance}%"></div>
                    </div>
                    <div class="progress-text">${student.days_present}/${student.total_days}</div>
                </div>
            </td>
            <td>
                <button class="table-action-btn view-btn" title="View Profile"
                    data-name="${student.name}" data-roll="${student.roll_no}"
                    data-parent="${student.parent}" data-attendance="${student.attendance}"
                    data-initials="${student.initials}">
                    <i class="fa-solid fa-eye"></i>
                </button>
                <button class="table-action-btn edit-btn" title="Edit"
                    data-name="${student.name}" data-roll="${student.roll_no}">
                    <i class="fa-solid fa-pen"></i>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    // Re-initialize dynamic elements
    initProgressBars();
    initModalButtons();
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}