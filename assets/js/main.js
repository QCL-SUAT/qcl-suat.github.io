// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
  const toggle = document.querySelector('.menu-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (toggle && navLinks) {
    toggle.addEventListener('click', function() {
      navLinks.classList.toggle('open');
    });
  }

  // Mobile dropdown toggle (touch devices)
  const dropdownItems = document.querySelectorAll('.nav-item--has-dropdown');
  dropdownItems.forEach(function(item) {
    item.addEventListener('click', function(e) {
      if (window.innerWidth <= 768) {
        const link = item.querySelector(':scope > a');
        if (e.target === link) {
          e.preventDefault();
          item.classList.toggle('open');
        }
      }
    });
  });
});
