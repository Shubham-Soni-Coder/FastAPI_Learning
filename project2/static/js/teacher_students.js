document.addEventListener('DOMContentLoaded', () => {
    // Progress Bar Init
    document.querySelectorAll('.progress-bar-fill[data-width]').forEach(bar => {
        bar.style.width = bar.dataset.width + '%';
    });

    // Month Selector Logic
    const months = document.querySelectorAll('.month-item');
    months.forEach(month => {
        month.addEventListener('click', () => {
            months.forEach(m => m.classList.remove('active'));
            month.classList.add('active');
        });
    });

    // Modal Logic
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

    // Close Modal on Outside Click
    window.onclick = function (event) {
        if (event.target == viewModal) {
            viewModal.style.display = "none";
        }
        if (event.target == editModal) {
            editModal.style.display = "none";
        }
    }
});

function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}
