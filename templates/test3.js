function redirectToForm() {
    var session = document.getElementById('sessionDropdown').value;
    if (session) {
        window.location.href = 'test2.html?session=' + session;
    } else {
        alert('Please select a session.');
    }
}