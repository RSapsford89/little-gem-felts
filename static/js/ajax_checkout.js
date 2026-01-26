document.addEventListener('DOMContentLoaded', function() {
    // This code is based upon the basket JS which uses AJAX
    const shipForm = document.getElementById('shipping-form');
    const dataUrl= shipForm.getAttribute('data-url')
    if (!shipForm) return;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    shipForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(shipForm);

        fetch(dataUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                disableForm('#shipping-form');
                // Optionally show a success message
            } else {
                alert('Error: ' + (data.error || data.message));
            }
        })
        .catch(error => {
            alert('Failed to submit form.');
            console.log(error);
        });
    });
    //disableForm from AI
    function disableForm(formSelector) {
        const form = document.querySelector(formSelector);
        if (!form) return;
        form.querySelectorAll('input, select, textarea, button').forEach(el => {
            el.disabled = true;
        });
        form.classList.add('form-disabled');
    }
});//eof