document.addEventListener('DOMContentLoaded', function() {
    const addButton = document.getElementById('add-img-btn');
    // const container = document.querySelector('.product-listing form'); 
    const totalForms = document.getElementById('id_images-TOTAL_FORMS');
    const MAX_FORMS = 8;

    addButton.addEventListener('click', function() {
        let formCount = parseInt(totalForms.value);

        if (formCount < MAX_FORMS) {
            // Find the last form to clone it
            const forms = document.getElementsByClassName('image-form');
            const lastForm = forms[forms.length - 1];
            const newForm = lastForm.cloneNode(true);

            // Update indices in the new form (e.g., images-0 to images-1)
            const formRegex = new RegExp(`images-(\\d+)-`, 'g');
            newForm.innerHTML = newForm.innerHTML.replace(formRegex, `images-${formCount}-`);

            // Clear values in the new form
            const inputs = newForm.querySelectorAll('input');
            inputs.forEach(input => {
                if (input.type === 'file') input.value = '';
                if (input.type === 'checkbox') input.checked = false;
                if (input.type === 'number') input.value = '';
            });

            // Remove the "Current image" preview from the clone if it exists
            const currentImg = newForm.querySelector('.current-image');
            if (currentImg) currentImg.remove();

            // Insert before the buttons
            addButton.parentNode.insertBefore(newForm, addButton);

            // Update the management form count
            totalForms.value = formCount + 1;

            // Hide button if we reached the limit
            if (formCount + 1 >= MAX_FORMS) {
                addButton.style.display = 'none';
            }
        }
    });
});