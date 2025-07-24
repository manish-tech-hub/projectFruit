document.addEventListener('DOMContentLoaded', function() {
  const hamburgerBtn = document.getElementById('hamburger-btn');
  const navLinks = document.getElementById('nav-links');
  const hamburgerIcon = hamburgerBtn.querySelector('i');

  hamburgerBtn.addEventListener('click', function() {
    navLinks.classList.toggle('show');
    
    // Toggle between hamburger and close icon
    if (navLinks.classList.contains('show')) {
      hamburgerIcon.classList.remove('fa-bars');
      hamburgerIcon.classList.add('fa-times');
    } else {
      hamburgerIcon.classList.remove('fa-times');
      hamburgerIcon.classList.add('fa-bars');
    }
  });
});