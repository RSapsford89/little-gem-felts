document.addEventListener('DOMContentLoaded', function(){
    const plusButtons = document.querySelectorAll('wa-button[data-action="increase"]');
    const minusButtons = document.querySelectorAll('wa-button[data-action="decrease"]');

    plusButtons.forEach(button=>{
        button.addEventListener('click', function(e){
            e.preventDefault();
            const btnAction = button.getAttribute('data-action');
            const btnId = button.getAttribute('data-item-id');
            const quantityInput = document.querySelector(`.qty-input[data-item-id="${btnId}"]`);
            let currentQty = parseInt(quantityInput.getAttribute('data-qty'));
            currentQty += 1;
            console.log(currentQty);
            // incrementDecrement(quantityInput, currentQty);
            quantityInput.value = currentQty;
        });
    });

    minusButtons.forEach(button=>{
        button.addEventListener('click', function(e){
            e.preventDefault();
            const btnAction = button.getAttribute('data-action');
            const btnId = button.getAttribute('data-item-id');
            const quantityInput = document.querySelector(`.qty-input[data-item-id="${btnId}"]`);
            let currentQty = parseInt(quantityInput.getAttribute('data-qty'));
            currentQty -= 1;
            console.log(currentQty);
            // incrementDecrement(quantityInput, currentQty);
            quantityInput.value = currentQty;
        });
    });

    function incrementDecrement(qtyInput, currentInputValue){
        qtyInput.value = currentInputValue;
    }
});