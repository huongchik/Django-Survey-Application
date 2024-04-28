document.addEventListener('DOMContentLoaded', function() {
    const dependentOnSelect = document.querySelector('#id_dependent_on');
    const requiredAnswersSelect = document.querySelector('#id_required_answers');

    dependentOnSelect.addEventListener('change', function() {
        const questionId = dependentOnSelect.value;
        if (questionId) {
            fetch(`/surveys/questions/${questionId}/answers/`)  // Adjusted path
                .then(response => response.json())
                .then(data => {
                    requiredAnswersSelect.innerHTML = '';
                    data.forEach(answer => {
                        const option = new Option(answer.text, answer.id, false, false);
                        requiredAnswersSelect.appendChild(option);
                    });
                })
                .catch(error => console.log('Error:', error));
        } else {
            requiredAnswersSelect.innerHTML = '';
        }
    });
});
