// script.js

// You can add JavaScript code here to handle client-side interactions
// This is just a placeholder/example

// For example, you can add client-side form validation
document.addEventListener('DOMContentLoaded', function () {
    const registrationForm = document.querySelector('#registration-form');
    if (registrationForm) {
        registrationForm.addEventListener('submit', function (event) {
            const usernameInput = document.querySelector('#username');
            const passwordInput = document.querySelector('#password');
            
            if (usernameInput.value.trim() === '') {
                alert('Please enter a username.');
                event.preventDefault();
            }
            if (passwordInput.value.trim() === '') {
                alert('Please enter a password.');
                event.preventDefault();
            }
        });
    }
});
