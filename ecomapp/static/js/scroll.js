document.addEventListener("DOMContentLoaded", function() {
    document.querySelector('a[href="#footer"]').addEventListener("click", function(event) {
        event.preventDefault(); // Stop default jump behavior
        document.querySelector(".footer").scrollIntoView({
            behavior: "smooth"
        });
    });
});