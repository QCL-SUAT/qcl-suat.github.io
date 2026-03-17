// Theme toggle (runs immediately to prevent flash)
(function() {
  var saved = localStorage.getItem('qcl-theme');
  if (saved === 'light') {
    document.documentElement.setAttribute('data-theme', 'light');
  }
})();

function toggleTheme() {
  var current = document.documentElement.getAttribute('data-theme');
  var next = current === 'light' ? 'dark' : 'light';
  if (next === 'dark') {
    document.documentElement.removeAttribute('data-theme');
  } else {
    document.documentElement.setAttribute('data-theme', 'light');
  }
  localStorage.setItem('qcl-theme', next);
  updateThemeIcon(next);
}

function updateThemeIcon(theme) {
  var btn = document.querySelector('.theme-toggle');
  if (btn) btn.textContent = theme === 'light' ? '☀️' : '🌙';
}

// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
  // Set theme icon on load
  var saved = localStorage.getItem('qcl-theme') || 'dark';
  updateThemeIcon(saved);

  var toggle = document.querySelector('.menu-toggle');
  var navLinks = document.querySelector('.nav-links');

  if (toggle && navLinks) {
    toggle.addEventListener('click', function() {
      navLinks.classList.toggle('open');
    });
  }

  // Mobile dropdown toggle (touch devices)
  var dropdownItems = document.querySelectorAll('.nav-item--has-dropdown');
  dropdownItems.forEach(function(item) {
    item.addEventListener('click', function(e) {
      if (window.innerWidth <= 768) {
        var link = item.querySelector(':scope > a');
        if (e.target === link) {
          e.preventDefault();
          item.classList.toggle('open');
        }
      }
    });
  });
});
