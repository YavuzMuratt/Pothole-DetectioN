function getMarkerColor(status) {
    switch (status) {
        case 'New':
            return 'red';
        case 'In Progress':
            return 'orange';
        case 'Done':
            return 'green';
        default:
            return 'blue';
    }
}

var map = L.map('map').setView([0, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

fetch('/potholes')
    .then(response => response.json())
    .then(data => {
        if (data.length > 0) {
            var bounds = [];
            data.forEach(pothole => {
                var markerColor = getMarkerColor(pothole.status);
                var marker = L.circleMarker([pothole.latitude, pothole.longitude], {
                    color: markerColor,
                    radius: 10
                }).addTo(map);

                marker.bindPopup(
                    `<b>Pothole ID:</b> ${pothole.id}<br>
                     <b>Address:</b> ${pothole.address}<br>
                     <b>Status:</b> ${pothole.status}<br>
                     <img src="/pothole/image/${pothole.id}" alt="Pothole Image" style="width:100px;">`
                );
                bounds.push([pothole.latitude, pothole.longitude]);
            });
            map.fitBounds(bounds);
        } else {
            alert('No potholes detected yet.');
        }
    })
    .catch(error => console.error('Error fetching pothole data:', error));
