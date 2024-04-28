
document.addEventListener('DOMContentLoaded', function () {
    const questions = Array.from(document.querySelectorAll('.question'));
    const form = document.querySelector('form');

    form.addEventListener('submit', function (event) {
        let isValid = true;
        document.querySelectorAll('.question').forEach(question => {
            const inputs = question.querySelectorAll('input[type="text"], input[type="radio"], input[type="checkbox"]');
            const isRequired = question.dataset.required === 'True';
            let hasAnswer = Array.from(inputs).some(input => {
                return (input.type === 'checkbox' || input.type === 'radio') ? input.checked : input.value.trim() !== '';
            });

            if (isRequired && !hasAnswer) {
                question.querySelector('.error-message').style.display = 'block';
                question.style.border = '2px solid red'; // Add red border to question
                isValid = false;
            } else {
                question.querySelector('.error-message').style.display = 'none';
                question.style.border = '1px solid #ccc'; // Revert to original border
            }
        });

        if (!isValid) {
            event.preventDefault(); // Prevent form submission if not valid
        }
    });
    function updateVisibility() {
        questions.forEach(question => {
            const dependency = question.dataset.dependentOn;
            const requiredAnswers = question.dataset.requiredAnswers ? question.dataset.requiredAnswers.split(',').map(answer => answer.trim().toLowerCase()) : [];

            if (dependency && requiredAnswers.length) {
                let parentAnswers = new Set();
                // Collect values from all relevant inputs (text, radio, checkbox)
                document.querySelectorAll(`input[name="${dependency}"], input[name="${dependency}[]"]`).forEach(input => {
                    if ((input.type === 'radio' || input.type === 'checkbox') && input.checked) {
                        parentAnswers.add(input.value.toLowerCase());
                    } else if (input.type === 'text' && input.value.trim()) {
                        parentAnswers.add(input.value.trim().toLowerCase());
                    }
                });

                // Determine if the sets of required and parent answers match exactly for multiple-choice
                const parentAnswersArray = Array.from(parentAnswers);
                const isExactMatch = requiredAnswers.length === parentAnswersArray.length && requiredAnswers.every(answer => parentAnswers.has(answer));

                // Update display based on exact match of required answers
                question.style.display = isExactMatch ? 'block' : 'none';
            } else {
                question.style.display = 'block'; // Display questions that have no dependencies
            }
        });
    }

    // Attach change and input event listeners for dynamic update
    document.querySelectorAll('input[type="text"], input[type="radio"], input[type="checkbox"]').forEach(input => {
        input.addEventListener('change', updateVisibility);
        if (input.type === 'text') {
            input.addEventListener('input', updateVisibility);
        }
    });

    updateVisibility(); // Perform an initial update on page load
});
