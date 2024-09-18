let potholesData = [];

// Fetch and display pothole data
function fetchAndDisplayPotholes() {
    fetch('/potholes')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(data); // Log the fetched data
            potholesData = data;
            filterAndSearchPotholes(); // Call the filtering function to display data
        })
        .catch(error => console.error('Error fetching pothole data:', error));
}

// Filter and search potholes based on the status and search input
function filterAndSearchPotholes() {
    const tableBody = document.getElementById('pothole-data');
    const statusFilter = document.getElementById('statusFilter').value;
    const searchInput = document.getElementById('searchInput').value.toLowerCase();

    tableBody.innerHTML = ''; // Clear the existing rows

    potholesData.forEach(pothole => {
        const matchesStatus = (statusFilter === 'All' || pothole.status === statusFilter);
        const matchesSearch = (
            pothole.id.toString().includes(searchInput) ||
            pothole.filename.toLowerCase().includes(searchInput) ||
            pothole.address.toLowerCase().includes(searchInput)
        );

        if (matchesStatus && matchesSearch) {
            const row = document.createElement('tr');

            row.innerHTML = `
                <td>${pothole.id}</td>
                <td>${pothole.filename}</td>
                <td>${pothole.date}</td>
                <td>${pothole.time}</td>
                <td>${pothole.latitude}</td>
                <td>${pothole.longitude}</td>
                <td>${pothole.address}</td>
                <td>
                    <button class="btn btn-info btn-sm" onclick="toggleImage(${pothole.id})">Show Image</button>
                    <div id="image-${pothole.id}" class="hidden-image">
                        <img src="/pothole/image/${pothole.id}" class="img-fluid" alt="Pothole Image">
                    </div>
                </td>
                <td id="status-${pothole.id}">${pothole.status || 'New'}</td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="updateStatus(${pothole.id}, 'In Progress')">In Progress</button>
                    <button class="btn btn-success btn-sm" onclick="updateStatus(${pothole.id}, 'Done')">Done</button>
                    <button class="btn btn-danger btn-sm" onclick="deletePothole(${pothole.id})">Delete</button>
                </td>
            `;

            tableBody.appendChild(row);
        }
    });
}

// Function to toggle image visibility
function toggleImage(id) {
    const imageDiv = document.getElementById(`image-${id}`);
    imageDiv.style.display = imageDiv.style.display === 'none' || imageDiv.style.display === '' ? 'block' : 'none';
}

// Function to update the status of a pothole
function updateStatus(pothole_id, status) {
    console.log(`Updating status of pothole ${pothole_id} to ${status}`); // Debugging log
    fetch(`/pothole/${pothole_id}/update_status`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `status=${status}`,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Server response:', data); // Log the server response
        if (data.success) {
            // Update the status directly in the DOM
            const statusCell = document.getElementById(`status-${pothole_id}`);
            statusCell.textContent = data.status;
        } else {
            alert('Failed to update status');
        }
    })
    .catch(error => {
        console.error('Error in updateStatus:', error); // Log any errors
    });
}

// Function to delete a pothole
function deletePothole(pothole_id) {
    if (confirm('Are you sure you want to delete this pothole?')) {
        console.log(`Deleting pothole ${pothole_id}`); // Debugging log
        fetch(`/pothole/${pothole_id}/delete`, {
            method: 'POST'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Server response:', data); // Log the server response
            if (data.success) {
                // Refresh the data list after deletion
                fetchAndDisplayPotholes();
            } else {
                alert('Failed to delete pothole');
            }
        })
        .catch(error => {
            console.error('Error in deletePothole:', error); // Log any errors
        });
    }
}

// Call fetchAndDisplayPotholes to load data on page load
fetchAndDisplayPotholes();
