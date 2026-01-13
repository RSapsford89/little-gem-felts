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
                            <wa-input class='qty-input' placeholder='3' data-item-id="1" data-qty="3">
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
                            <wa-input class='qty-input' placeholder='2' data-item-id="2" data-qty="2">
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
    });

    afterEach(()=>{
        document.body.innerHTML = '';
    });

    test('to find all plus buttons',()=>{
        expect(plusButtons.length).toBeGreaterThan(0);
        // console.log('Plus buttons found:', plusButtons.length);
    });

// Up to line 57: this set up was generated through AI prompt.

    test('to find all minus buttons',()=>{
            expect(plusButtons.length).toBe(2);
            // console.log('Minus buttons found:', plusButtons.length);
        });

    test('to find placeholder values',()=>{
        // console.log('Number of Inputs:', quantityInputs.length);
        // console.log('Input value:', quantityInputs[1].getAttribute('placeholder'));
            expect(quantityInputs[1].getAttribute('placeholder')).toBe('2');
        });

    test('the qty input increases by 1 when related button is pressed',()=>{
        require('../../../../static/js/basket.js');
        const event = new Event("DOMContentLoaded");
        document.dispatchEvent(event);

        plusButtons[0].click();
        expect(quantityInputs[0].value).toBe(4);
        expect(quantityInputs[1].value).toBe(undefined);
    });

    test('the qty input decreases by 1 when related button is pressed',()=>{
        require('../../../../static/js/basket.js');
        const event = new Event("DOMContentLoaded");
        document.dispatchEvent(event);
        // this test fails because the placeholder value is used. Instead
        // the code should be updated to use data-id's to relate cards
        // together. 
        console.log('initial input0 value:',quantityInputs[0].value);
        console.log('initial input1 value:',quantityInputs[1].value);
        // first button pressed
        minusButtons[0].click();
        input0 = parseInt(quantityInputs[0].getAttribute('placeholder'));
        input1 = quantityInputs[1].value;

        console.log('btn0 pressed input0 value:',quantityInputs[0].value);
        console.log('btn0 pressed input1 value:',quantityInputs[1].value);
        expect(quantityInputs[0].value).toBe(input0 -1);//3-1
        expect(quantityInputs[1].value).toBe(input1);

        // second button pressed
        minusButtons[1].click();
        console.log('input0 value:',quantityInputs[0].value);
        console.log('input1 value:',quantityInputs[1].value);
        expect(quantityInputs[0].value).toBe(2);//3-1
        expect(quantityInputs[1].value).toBe(1);//2-1
    });
});//end of file