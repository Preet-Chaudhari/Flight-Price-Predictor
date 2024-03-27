

function fetchPrice() {
    event.preventDefault();
    let airline = document.getElementById('airline').value;
    let departure = document.getElementById('departure').value;
    let stops = document.getElementById('stop').value;
    let cabin_class = document.getElementById('cabin_class').value;
    let duration = document.getElementById('duration').value;
    let days_left = document.getElementById('days_left').value;

    fetch('/predict?' + new URLSearchParams({
        airline: airline,
        departure: departure,
        stops: stops,
        cabin_class: cabin_class,
        duration: duration,
        days_left: days_left,
    }, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }))
        .then(response => response.json())
        .then(data => {
            document.getElementById('price-result').innerText = 'Predicted Flight Price: ₹' + data["prediction"];
        })
        .catch(error => {
            console.error('Error:', error);
        });
}