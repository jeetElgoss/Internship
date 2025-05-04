// Populate year dropdown
        const currentYear = new Date().getFullYear();
        const yearDropdown = document.getElementById('yearDropdown');
        for (let year = currentYear; year <= currentYear +10 ; year++) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            yearDropdown.appendChild(option);
        }

        // Notification function
        function showNotification(message, type = 'info') {
            const notificationContainer = document.createElement('div');
            notificationContainer.className = `notification ${type}`;
            notificationContainer.innerHTML = `
                <span>${message}</span>
                <button class="close-btn">×</button>
            `;

            document.body.appendChild(notificationContainer);

            // Auto-remove after 3 seconds
            setTimeout(() => {
                notificationContainer.classList.add('fade-out');
                setTimeout(() => notificationContainer.remove(), 300);
            }, 3000);

            // Close button functionality
            notificationContainer.querySelector('.close-btn').addEventListener('click', () => {
                notificationContainer.classList.add('fade-out');
                setTimeout(() => notificationContainer.remove(), 300);
            });
        }

        // Call Python function
function callPythonFunction() {
    const yearDropdown = document.getElementById('yearDropdown');
    const internDropdown = document.getElementById('internDropdown');
    const dropdownButton = document.getElementById('dropdownMenuButton');
    const resultDiv = document.getElementById('result');
    const selectedYear = yearDropdown.value;

    // Clear previous content
    internDropdown.innerHTML = '<li><a class="dropdown-item disabled" href="#">Select an intern</a></li>';
    dropdownButton.textContent = 'Select Intern'; // Reset button text
    resultDiv.innerHTML = '';

    // Validate year selection
    if (!selectedYear) {
        showNotification('Please select a year.', 'error');
        return;
    }

    // Make API call
    fetch('/get_intern_dropdown', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ year: selectedYear })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error); });
        }
        return response.json();
    })
    .then(data => {
        if (data.interns && data.interns.length > 0) {
            // Populate intern dropdown
            data.interns.forEach(intern => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.className = 'dropdown-item';
                a.href = `/intern?intern_id=${intern.intern_id}`;
                a.dataset.internId = intern.intern_id;
                const decodedInternId = atob(intern.intern_id);
                a.textContent = `${intern.name} (ID: ${decodedInternId})`;
                a.addEventListener('click', (e) => {
                    dropdownButton.textContent = a.textContent; // Update button text
                    internDropdown.querySelectorAll('.dropdown-item').forEach(item => {
                        item.classList.remove('active');
                    });
                    a.classList.add('active'); // Highlight selected item
                });
                li.appendChild(a);
                internDropdown.appendChild(li);
            });
            // Show success notification
            showNotification(data.message, 'success');
        } else {
            // Show info notification for no data
            showNotification(data.message || 'No interns found for year ' + selectedYear, 'info');
        }
    })
    .catch(error => {
        // Show error notification
        showNotification(`Error: ${error.message}`, 'error');
    });
}