let index = 0;
const slides = document.querySelector('.slides');
const totalSlides = document.querySelectorAll('.slide').length;
const slideWidth = document.querySelector('.slide').offsetWidth; // Dynamically calculate slide width

// Move the slides every 4 seconds
function nextSlide() {
    index++;
    slides.style.transition = "transform 0.5s ease-in-out";
    slides.style.transform = `translateX(-${index * slideWidth}px)`; // Adjust to dynamic width

    // When reaching the last slide, reset to first slide
    if (index === totalSlides) {
        setTimeout(() => {
            slides.style.transition = "none"; // Disable transition for instant reset
            slides.style.transform = `translateX(0px)`; // Reset to first slide
            index = 0;
        }, 500); // Wait for transition to complete
    }
}

setInterval(nextSlide, 4000);


