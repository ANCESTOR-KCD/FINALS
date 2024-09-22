document.addEventListener("DOMContentLoaded", function() {
    // Check if form is saved for this session
    const params = new URLSearchParams(window.location.search);
    const session = params.get('session');
    if (session) {
        loadFormData(session);
    }
});

function loadFormData(session) {
    try {
        var formData = localStorage.getItem('formData_' + session);
        if (formData) {
            formData = JSON.parse(formData);
            document.getElementById('fullName').value = formData.fullName || '';
            document.getElementById('dob').value = formData.dob || '';
            document.getElementById('email').value = formData.email || '';
            document.getElementById('phone').value = formData.phone || '';

            // Load and display the image if it's saved
            if (formData.image) {
                var image = new Image();
                image.src = formData.image;
                image.alt = "Uploaded Document";
                document.getElementById('preview').appendChild(image);
            }
        }
    } catch (error) {
        console.error("Error loading form data: ", error);
    }
}

function previewImage(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = new Image();
            img.src = e.target.result;
            img.alt = "Uploaded Document Preview";
            document.getElementById('preview').innerHTML = ''; // Clear previous previews
            document.getElementById('preview').appendChild(img); // Add preview
            localStorage.setItem('formImage', e.target.result); // Save image as Base64 in localStorage
        };
        reader.readAsDataURL(file);
    }
}

document.getElementById('saveButton').addEventListener('click', function() {
    var selectedSession = document.getElementById('sessionDropdown').value;
    if (selectedSession) {
        try {
            var formData = {
                fullName: document.getElementById('fullName').value,
                dob: document.getElementById('dob').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                image: localStorage.getItem('formImage') || "" // Retrieve Base64 image from localStorage
            };

            localStorage.setItem('formData_' + selectedSession, JSON.stringify(formData));
            alert('Form data saved for session ' + selectedSession);
        } catch (error) {
            console.error("Error saving form data: ", error);
            alert("Failed to save the form data. Please try again.");
        }
    } else {
        alert('Please select a session.');
    }
});

function printForm(session) {
    var formData = localStorage.getItem('formData_' + session);
    if (formData) {
        formData = JSON.parse(formData);

        var printWindow = window.open('', '', 'width=800,height=600');
        printWindow.document.write('<html><head><title>Print Form</title></head><body>');
        printWindow.document.write('<h1>Form Data for Session ' + session + '</h1>');
        printWindow.document.write('<p>Full Name: ' + formData.fullName + '</p>');
        printWindow.document.write('<p>Date of Birth: ' + formData.dob + '</p>');
        printWindow.document.write('<p>Email: ' + formData.email + '</p>');
        printWindow.document.write('<p>Phone: ' + formData.phone + '</p>');

        // Add image if exists
        if (formData.image) {
            printWindow.document.write('<img src="' + formData.image + '" style="max-width: 100px; height: auto;">');
        }

        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.print();
    }
}