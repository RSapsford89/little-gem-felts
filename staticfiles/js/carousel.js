
// based heavily on the code from: https://www.w3schools.com/howto/howto_js_slideshow.asp
document.addEventListener('DOMContentLoaded', function() {
    let slideIndex = 1;
    
    // Initial call to show the first slide
    showSlides(slideIndex);

    // Attach Event Listeners (Best Practice)
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            plusSlides(-1);
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            plusSlides(1);
        });
    }

    function plusSlides(n) {
        showSlides(slideIndex += n);
    }

    function showSlides(n) {
        let i;
        let slides = document.getElementsByClassName("slides");
        
        // Safety check: if no slides exist, stop here to prevent errors
        if (slides.length === 0) return;

        if (n > slides.length) {slideIndex = 1}
        if (n < 1) {slideIndex = slides.length}

        // Hide all slides
        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
        }

        // Show the active slide
        // Note: slideIndex is 1-based, array is 0-based
        slides[slideIndex - 1].style.display = "block";
    }
});