console.log("message");
// Wrap the JavaScript code inside a function
function setupDateValidation() {
    var dateInput = document.getElementById('date-field');

    // Get the current date
    var currentDate = new Date().toISOString().split('T')[0];

    // Set the minimum date attribute to the current date
    dateInput.setAttribute('min', currentDate);

    // Event listener to validate date selection
    dateInput.addEventListener('input', function() {
        var selectedDate = dateInput.value;
        
        // Compare the selected date with the current date
        if (selectedDate > currentDate) {
            alert('Please select a date that is not in the future.');
            dateInput.value = currentDate; // Reset the value to current date
        }
    });
}

// Call the function after the DOM has been fully loaded
document.addEventListener("DOMContentLoaded", function() {
    setupDateValidation();
});
