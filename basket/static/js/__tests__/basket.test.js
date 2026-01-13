describe('Basket Quantity Controls', () => {
    let container;
    let plusButtons;
    let minusButtons;
    let quantityInputs;

    beforeEach(() => {
        // Setup DOM structure
        document.body.innerHTML = `
            <div class="horizontal-card-container">
                <div data-basket-item="1">
                    <wa-card>
                        <wa-button-group>
                            <wa-button data-action="decrease" data-item-id="1">
                                <wa-icon name='minus' class='minus-btn'></wa-icon>
                            </wa-button>
                            <wa-input class='qty-input' value='3' data-item-id="1" data-qty="3">
                                <wa-label slot="start">Qty</wa-label>
                            </wa-input>
                            <wa-button data-action="increase" data-item-id="1">
                                <wa-icon name='plus' class='plus-btn'></wa-icon>
                            </wa-button>
                        </wa-button-group>
                    </wa-card>
                </div>
                <div data-basket-item="2">
                    <wa-card>
                        <wa-button-group>
                            <wa-button data-action="decrease" data-item-id="2">
                                <wa-icon name='minus' class='minus-btn'></wa-icon>
                            </wa-button>
                            <wa-input class='qty-input' value='2' data-item-id="2" data-qty="2">
                                <wa-label slot="start">Qty</wa-label>
                            </wa-input>
                            <wa-button data-action="increase" data-item-id="2">
                                <wa-icon name='plus' class='plus-btn'></wa-icon>
                            </wa-button>
                        </wa-button-group>
                    </wa-card>
                </div>
            </div>
        `;

        plusButtons = document.querySelectorAll('.plus-btn');
        minusButtons = document.querySelectorAll('.minus-btn');
        quantityInputs = document.querySelectorAll('.qty-input');
        // Set the .value property on web components as custom
        //components attribute like standard components
        quantityInputs[0].value = '3';
        quantityInputs[1].value = '2';
    });

    afterEach(()=>{
        document.body.innerHTML = '';
    });

    test('to find all plus buttons',()=>{
        expect(plusButtons.length).toBeGreaterThan(0);
    });

// Up to line 57: this set up was generated through AI prompt.

    test('to find all minus buttons',()=>{
        expect(plusButtons.length).toBe(2);
    });

    test('to find input values',()=>{
        expect(quantityInputs[1].getAttribute('value')).toBe('2');
    });

    test('the qty input increases by 1 when related button is pressed',()=>{
        require('../../../../static/js/basket.js');
        const event = new Event("DOMContentLoaded");
        document.dispatchEvent(event);

        const plusButton1 = document.querySelector('wa-button[data-action="increase"][data-item-id="1"]');
        const plusButton2 = document.querySelector('wa-button[data-action="increase"][data-item-id="2"]');

        // first button pressed - read the data-qty for comparison
        plusButton1.click();
        input0 = parseInt(quantityInputs[0].getAttribute('data-qty'));//3
        input1 = parseInt(quantityInputs[1].getAttribute('data-qty'));//2

        expect(quantityInputs[0].value).toBe(input0 +1);//3 + 1 = 4
        expect(parseInt(quantityInputs[1].value)).toBe(input1);// unchanged 2

        // second button pressed
        plusButton2.click();
        expect(quantityInputs[0].value).toBe(4);// unchanged 4
        expect(quantityInputs[1].value).toBe(3);// 2 + 1 =3
    });

    test('the qty input decreases by 1 when related button is pressed',()=>{
        require('../../../../static/js/basket.js');
        const event = new Event("DOMContentLoaded");
        document.dispatchEvent(event);
        //access each button separately with querySelector + the data-item-id
        const minusButton1 = document.querySelector('wa-button[data-action="decrease"][data-item-id="1"]');
        const minusButton2 = document.querySelector('wa-button[data-action="decrease"][data-item-id="2"]');

        // first button pressed - read the data-qty for comparison
        minusButton1.click();
        input0 = parseInt(quantityInputs[0].getAttribute('data-qty'));//3
        input1 = parseInt(quantityInputs[1].getAttribute('data-qty'));//2

        expect(quantityInputs[0].value).toBe(input0 -1);
        expect(parseInt(quantityInputs[1].value)).toBe(input1);

        // second button pressed
        minusButton2.click();
        expect(quantityInputs[0].value).toBe(2);
        expect(quantityInputs[1].value).toBe(1);
    });

    test('the attributes  data-qty and data-item-id are read correctly',()=>{
        require('../../../../static/js/basket.js');
        const event = new Event("DOMContentLoaded");
        document.dispatchEvent(event);
        const plusButtons = document.querySelectorAll('wa-button[data-action="increase"][data-item-id="1"]');
        // gather the attributes
        expect(quantityInputs[0].getAttribute('data-qty')).toBe('3');
        expect(quantityInputs[1].getAttribute('data-qty')).toBe('2');
        expect(quantityInputs[0].getAttribute('data-item-id')).toBe('1');
        expect(quantityInputs[1].getAttribute('data-item-id')).toBe('2');
        // console.log(`qtyInput id is:`,${quantityInput});
    });
});//end of file