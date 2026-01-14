document.addEventListener('DOMContentLoaded', function(){
    const plusButtons = document.querySelectorAll('wa-button[data-action="increase"]');
    const minusButtons = document.querySelectorAll('wa-button[data-action="decrease"]');

    plusButtons.forEach(button=>{
        button.addEventListener('click', function(e){
            e.preventDefault();
            const btnId = button.getAttribute('data-item-id');
            const quantityInput = document.querySelector(`.qty-input[data-item-id="${btnId}"]`);
            let currentQty = parseInt(quantityInput.getAttribute('data-qty'));
            // console.log(`initial qty is:,${quantityInput.value}`);
            const newVal = incrementDecrement(true, currentQty);
            
            quantityInput.setAttribute('value',newVal); 
            quantityInput.setAttribute('data-qty',newVal); 
            // console.log(`sent true, inputValue is, ${quantityInput.value}`);
        });
    });

    minusButtons.forEach(button=>{
        button.addEventListener('click', function(e){
            e.preventDefault();
            const btnId = button.getAttribute('data-item-id');
            const quantityInput = document.querySelector(`.qty-input[data-item-id="${btnId}"]`);
            let currentQty = parseInt(quantityInput.getAttribute('data-qty'));
            
            // console.log(`initial qty is:,${quantityInput.value}`);
            const newVal = incrementDecrement(false, currentQty);
            quantityInput.setAttribute('value',newVal);
            quantityInput.setAttribute('data-qty',newVal); 
            // console.log(`sent false, inputValue is, ${quantityInput.value}`);
        });
    });
    
    function incrementDecrement(trueFalse, currentQty){
        if (trueFalse === true){
            currentQty +=1;
        }
        else if(trueFalse === false){
            currentQty -=1;
        }
        return currentQty;
    }
});
