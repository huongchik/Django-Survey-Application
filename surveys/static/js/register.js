document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('input[type="text"], input[type="password"], input[type="email"]');

    inputs.forEach(input => {
        // Show helper text on input focus
        input.addEventListener('focus', function() {
            const helperText = input.nextElementSibling;
            if (helperText.classList.contains('helper-text')) {
                helperText.style.display = 'block';
            }
        });

        // Hide helper text when input loses focus
        input.addEventListener('blur', function() {
            const helperText = input.nextElementSibling;
            if (helperText.classList.contains('helper-text')) {
                helperText.style.display = 'none';
            }
        });

        // Optionally, show dynamic helper text as the user types, validate here
        input.addEventListener('input', function() {
            const helperText = input.nextElementSibling;
            // You can add validation logic here to update helper text dynamically
        });
    });
});
