document.addEventListener('DOMContentLoaded', (event) => {
    var slideIndex = 0;
    showSlides();
    
    function showSlides() {
        var i;
        var slides = document.getElementById("slideshow").getElementsByTagName("img");
        for (i = 0; i < slides.length; i++) {
            slides[i].classList.remove("active");  
        }
        slideIndex++;
        if (slideIndex > slides.length) {slideIndex = 1}    
        slides[slideIndex-1].classList.add("active");  
        setTimeout(showSlides, 2000); // Change image every 2 seconds
    }
})

document.addEventListener('DOMContentLoaded', (event) => {
window.onload = function() {
    var slides = document.getElementById("slideshow").getElementsByTagName("img");
    var totalSlides = slides.length;
    for (var i = 0; i < totalSlides; i++) {
        slides[i].style.animationDelay = (i * 2) + 's'; // Change '2' to the duration of your animation
    }
}
})