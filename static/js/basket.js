document.addEventListener('DOMContentLoaded', function(){
    const plusButtons = document.querySelectorAll('wa-button[data-action="increase"]');
    const minusButtons = document.querySelectorAll('wa-button[data-action="decrease"]');
    const removeButtons = document.querySelectorAll('wa-button[data-action="remove"]');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

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

    removeButtons.forEach(button=>{
        button.addEventListener('click', function(e){
            e.preventDefault();
            const btnId = button.getAttribute('data-item-id');
            const item = document.querySelector(`[data-item-id="${btnId}"]`);
            
            //csrf from the top, remove from basket, remove from context/session

            fetch(`/basket/remove/${btnId}`,{
                method: 'POST',
                headers:{
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if(data.success){
                    $item.remove();
                    
                }
            })

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
