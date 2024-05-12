document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('userForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Get the values from the form inputs
        var userID = document.getElementById('userID').value;
        var roomCode = document.getElementById('roomCode').value;

        // Create a JSON object with the user ID and room code
        var userData = {
            "userID": userID,
            "roomCode": roomCode
        };
        window.location.href = '/chat?room=' + roomCode + '&userID=' + userID;

        // Convert the JSON object to a string
        var jsonData = JSON.stringify(userData);

        // Send an AJAX POST request to the server
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/update_data", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                console.log("Data updated successfully!");
            }
        };
        xhr.send(jsonData);

    });
});

