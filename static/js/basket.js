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
            updateBasket(btnId,newVal);
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
            updateBasket(btnId,newVal);
        });
    });
//implementation of the fetch and promises created with help of AI.
    removeButtons.forEach(button=>{
        button.addEventListener('click', function(e){
            e.preventDefault();
            const btnId = button.getAttribute('data-item-id');
            const item = document.querySelector(`[data-item-id="${btnId}"]`);            
            //csrf from the top, remove from basket, remove from context/session
            fetch(`/basket/remove/${btnId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if(data.success){
                    item.remove();
                    updateBasketTotals(data);
                    
                    const remainingItems = document.querySelectorAll('[data-item-id]').length;
                    if (remainingItems === 0) {
                        displayEmptyBasket();
                    }
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                alert('Failed to remove item. Reloading page...');
                console.log(error);
                location.reload();
            });
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
// this function was created with the help of AI on how to use
//fetch and format for xcrsftoken
    function updateBasket(productId, quantity){
        fetch(`/basket/update/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                quantity: quantity,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if(data.success){
                updateBasketTotals(data);
                document.querySelector(`.qty-input[data-item-id="${productId}"]`).value = data.quantity;
                // If the new quantity is 0 (or less), remove the HTML element
                if (quantity <= 0) {
                    const item = document.querySelector(`div[data-item-id="${productId}"]`);
                    if (item) {
                        item.remove();
                    }

                    // Check if that was the last item
                    const remainingItems = document.querySelectorAll('div[data-item-id]').length;
                    if (remainingItems === 0) {
                        location.reload(); 
                    }
                }

                showToast(data.message, 'success');
            } else {
                showToast(data.message, 'error');
                location.reload();
            }
        })
        .catch(error => {
            console.log(error);
        });       
    }

    function updateBasketTotals(data){
        //update each element with the new basket context
        const totalItems = document.querySelector('td[data-id="totalItems"]');
        const subtotal = document.querySelector('td[data-id="subtotal"]');
        const delivery = document.querySelector('td[data-id="delivery"]');
        const grandTotal = document.querySelector('td[data-id="grandTotal"]');

        totalItems.textContent=data.product_count
        subtotal.textContent=data.total
        delivery.textContent=data.delivery
        grandTotal.textContent=data.grand_total
    }

});//end of file
