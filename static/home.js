// Create particles
function createParticles() {
    const particlesContainer = document.getElementById('particles');
    const particleCount = 20;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        
        // Random size between 5px and 20px
        const size = Math.random() * 15 + 5;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        // Random position
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        particle.style.left = `${posX}%`;
        particle.style.top = `${posY}%`;
        
        // Random animation duration between 15s and 30s
        const duration = Math.random() * 15 + 15;
        particle.style.animationDuration = `${duration}s`;
        
        // Random delay
        const delay = Math.random() * 5;
        particle.style.animationDelay = `${delay}s`;
        
        particlesContainer.appendChild(particle);
    }
}

// Initialize particles
createParticles();

// Custom Alert System
function showAlert(message, type = 'info') {
    const alert = document.getElementById('customAlert');
    const overlay = document.getElementById('alertOverlay');
    const messageEl = document.getElementById('alertMessage');
    const iconEl = alert.querySelector('.custom-alert-icon i');
    
    // Set icon based on type
    switch(type) {
        case 'success':
            iconEl.className = 'fas fa-check-circle';
            break;
        case 'error':
            iconEl.className = 'fas fa-exclamation-circle';
            break;
        case 'warning':
            iconEl.className = 'fas fa-exclamation-triangle';
            break;
        default:
            iconEl.className = 'fas fa-info-circle';
    }
    
    messageEl.textContent = message;
    overlay.classList.add('show');
    alert.classList.add('show');
    
    // Auto close after 5 seconds
    setTimeout(() => {
        hideAlert();
    }, 5000);
}

function hideAlert() {
    const alert = document.getElementById('customAlert');
    const overlay = document.getElementById('alertOverlay');
    alert.classList.remove('show');
    overlay.classList.remove('show');
}

// Close alert when clicking close button or overlay
document.getElementById('alertClose').addEventListener('click', hideAlert);
document.getElementById('alertOverlay').addEventListener('click', hideAlert);

// Wallet connection functionality
document.getElementById('connectButton').addEventListener('click', async () => {
    if (typeof window.ethereum !== 'undefined') {
        try {
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            window.location.href = '/dashboard';
        } catch (error) {
            console.error("Error connecting to wallet:", error);
            showAlert("Connection failed. Please try again.", "error");
        }
    } else {
        showAlert("MetaMask is not installed. Please install it to connect your wallet.", "warning");
    }
});

// Mobile menu functionality
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const mobileMenuClose = document.getElementById('mobileMenuClose');
const mobileMenu = document.getElementById('mobileMenu');
const mobileMenuLinks = document.querySelectorAll('.mobile-menu-link');

mobileMenuToggle.addEventListener('click', () => {
    mobileMenu.classList.add('active');
});

mobileMenuClose.addEventListener('click', () => {
    mobileMenu.classList.remove('active');
});

mobileMenuLinks.forEach(link => {
    link.addEventListener('click', () => {
        mobileMenu.classList.remove('active');
    });
});

// Navigation active state
const navLinks = document.querySelectorAll('.navbar-link');
const sections = document.querySelectorAll('.section');

function setActiveLink() {
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        
        if (window.pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}

window.addEventListener('scroll', setActiveLink);

// Contact form submission
const contactForm = document.getElementById('contactForm');

contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;
    
    // Here you would typically send the form data to your server
    console.log('Form submitted:', { name, email, message });
    
    showAlert('Thank you for your message! We will get back to you soon.', 'success');
    
    // Reset form
    contactForm.reset();
});