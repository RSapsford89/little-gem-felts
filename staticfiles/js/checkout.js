// Get Stripe public key and client secret from the page
document.addEventListener('DOMContentLoaded', function() {
const paymentForm = document.querySelector("#payment-form");

if (!paymentForm){
  console.error("Stripe payment form not found");
  showToast(data.error || "Stripe is unavailable", "error");
  return;
}

const stripePublicKey = paymentForm.dataset.stripePublicKey;
const clientSecret = paymentForm.dataset.clientSecret;
const stripe = Stripe(stripePublicKey);
const dataUrl = paymentForm.getAttribute('data-url')
let elements;

initialize();
checkStatus();
document.querySelector("#payment-form").addEventListener("submit", handleSubmit);

// Initialize Stripe elements with the client secret from Django
async function initialize() {
  const appearance = {
    theme: 'stripe',
  };
  elements = stripe.elements({ appearance, clientSecret });
  
  const paymentElementOptions = {
    layout: "accordion",
  };
  
  const paymentElement = elements.create("payment", paymentElementOptions);
  paymentElement.mount("#payment-element");
}

async function handleSubmit(e) {
  e.preventDefault();
  setLoading(true);
  
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const formData = new FormData(paymentForm)

  try {
      const response = await fetch(dataUrl,{
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData,
      });
      const data = await response.json();

      if(data.success){
        const { error } = await stripe.confirmPayment({
          elements,
          confirmParams: {
            return_url: window.location.origin +  "/order/confirmation/",
          },
        });

        if (error.type === "card_error" || error.type === "validation_error") {
          showToast("Stripe payment error", "error");
        } 
        else {
          showToast("An unexpected error has occured", "error");
        }
      }
      else{
        showToast("Order failed","error");
      }
      
  } 
  catch (error) {
    showToast("Unable to get Order from server", "error");
  }
  
  setLoading(false);

}

// ------- UI helpers -------
async function checkStatus() {
    const clientSecret = new URLSearchParams(window.location.search).get(
      "payment_intent_client_secret"
    );
    if (!clientSecret) return;

    const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);

    switch (paymentIntent.status) {
      case "succeeded": showToast("Payment successful"); break;
      case "processing": showToast("Your payment is processing.","info"); break;
      case "requires_payment_method": showToast("Your payment was not successful, please try again.","error"); break;
      default: showToast("Something went wrong.","error"); break;
    }
  }

function setLoading(isLoading) {
  if (isLoading) {
    document.querySelector("#submit").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("#submit").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
}

});