function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

var csrftoken = readCookie('csrftoken');

function getSlots() {
    var date = document.getElementById("booking-date").value;
    var data = {'date': date}
    var body = JSON.stringify(data);
    var options = {
        method: 'POST',
        body: body,
        headers: { 'content-type': 'application/json', 'X-CSRFToken': csrftoken },
        redirect: "follow"
    }
    fetch("/sports/api/getSlots/", options).then(response => {
        if (response.status == 200) {
            document.getElementById("already-booked").style.display = "none";
            document.getElementById("no-slot").style.display = "none";
            response.json().then(response => {
                document.getElementById("booking-slot-box").style.display = "flex";
                var slots = document.getElementById("booking-slot");
                slots.style.display = "flex"
                slots.innerHTML = '<option value="0">Select Slot</option>';
                response.slots.forEach(element => {
                    slots.innerHTML += `<option value="${element}">${element}</option>`;
                });
            })
        } else if (response.status == 403) {
            document.getElementById("already-booked").style.display = "none";
            document.getElementById("no-slot").style.display = "block";
            document.getElementById("booking-availability-box").style.display = "none";
            document.getElementById("booking-slot-box").style.display = "none";
            document.getElementById("booking-btn").style.display = "none";
        }
    });
}

function getAvailability() {
    var date = document.getElementById("booking-date").value;
    var time = document.getElementById("booking-slot").value;
    if (time == 0) {
        return false;
    }
    var data = {'date': date, 'time': time}
    var body = JSON.stringify(data);
    var options = {
        method: 'POST',
        body: body,
        headers: { 'content-type': 'application/json', 'X-CSRFToken': csrftoken },
        redirect: "follow"
    }
    fetch("/sports/api/getAvailability/", options).then(response => {
        if (response.status == 200) {
            document.getElementById("already-booked").style.display = "none";
            document.getElementById("no-slot").style.display = "none";
            document.getElementById("booking-btn").style.display = "block";
            response.json().then(response => {
                document.getElementById("booking-availability-box").style.display = "flex";
                var slots = document.getElementById("booking-availability");
                slots.style.display = "flex"
                response.availability.forEach(element => {
                    slots.innerHTML = `${element} Available`;
                });
            })
        } else if (response.status == 403) {
            document.getElementById("already-booked").style.display = "none";
            document.getElementById("no-slot").style.display = "block";
            document.getElementById("booking-availability-box").style.display = "none";
            document.getElementById("booking-slot-box").style.display = "none";
            document.getElementById("booking-btn").style.display = "none";
        } else if (response.status == 402) {
            document.getElementById("no-slot").style.display = "none";
            document.getElementById("already-booked").style.display = "block";
            document.getElementById("booking-availability-box").style.display = "none";
            document.getElementById("booking-btn").style.display = "none";
        }
    });
}