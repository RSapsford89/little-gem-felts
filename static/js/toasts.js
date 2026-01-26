function showToast(message, type='success'){
    // put any custom colour settings here as an object
    let colour;
    if(type ==='error' || type ==='danger'){
        colour = "linear-gradient(to right, #b05500, #e92720)"
    }
    else if(type ==='warning'){
        colour = "linear-gradient(to right, #ebe264, #f7aa04)"
    }
    else if(type ==='success'){
        colour = "linear-gradient(to right, #00b09b, #96c93d)"
    }
    Toastify({
        text: message,
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: "top", // `top` or `bottom`
        position: "right", // `left`, `center` or `right`
        stopOnFocus: true, // Prevents dismissing of toast on hover
        style: {
            background: colour,//put custom colors here
        },
        onClick: function(){} // Callback after click
    }).showToast();
};