document.addEventListener('DOMContentLoaded', function(){
    const plusButton = document.querySelectorAll('.plus-btn');
    const minusButton = document.querySelectorAll('.minus-btn');

    plusButton.forEach(button=>{
        button.addEventListener('click', function(e){
            e.preventDefault();
            const quantityInput = document.querySelector('.qty-input');
            let currentQty = parseInt(quantityInput.getAttribute('placeholder'));
            currentQty += 1;
            console.log(currentQty);
            incrementDecrement(quantityInput, currentQty);
        });
    });

    minusButton.forEach(button=>{
        button.addEventListener('click', function(e){
            e.preventDefault();
            const quantityInput = document.querySelector('.qty-input');
            let currentQty = parseInt(quantityInput.getAttribute('placeholder'));
            currentQty -= 1;
            console.log(currentQty);
            incrementDecrement(quantityInput, currentQty);
        });
    });

    function incrementDecrement(qtyInput, currentInputValue){
        qtyInput.value = currentInputValue;
    }
});