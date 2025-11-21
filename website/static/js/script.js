let navbar = document.querySelector('.header .flex .navbar');
let menuBtn = document.querySelector('#menu-btn');
let header = document.querySelector('.header');

// Smooth mobile menu toggle with animation
menuBtn.onclick = () => {
   navbar.classList.toggle('active');
   menuBtn.classList.toggle('fa-times'); // Change icon to close
}

// Close menu on scroll and add header scroll effect
window.onscroll = () => {
   navbar.classList.remove('active');
   menuBtn.classList.remove('fa-times');

   if (window.scrollY > 100) {
      header.classList.add('scrolled');
   } else {
      header.classList.remove('scrolled');
   }
}

// Input validation for number fields
document.querySelectorAll('input[type="number"]').forEach(inputNumber => {
   inputNumber.oninput = () =>{
      if(inputNumber.value.length > inputNumber.maxLength) inputNumber.value = inputNumber.value.slice(0, inputNumber.maxLength);
   };
});

// Job Search and Filter Functionality
document.addEventListener('DOMContentLoaded', function() {
   const searchInput = document.getElementById('job-search');
   const searchBtn = document.getElementById('search-btn');
   const locationFilter = document.getElementById('location-filter');
   const typeFilter = document.getElementById('type-filter');
   const salaryMinInput = document.getElementById('salary-min');
   const salaryMaxInput = document.getElementById('salary-max');
   const experienceFilter = document.getElementById('experience-filter');
   const skillsFilter = document.getElementById('skills-filter');
   const applyFiltersBtn = document.getElementById('apply-filters');
   const clearFiltersBtn = document.getElementById('clear-filters');
   const jobBoxes = document.querySelectorAll('.box-container .box');

   if (!searchInput || !jobBoxes.length) return; // Only run on jobs page

   function filterJobs() {
      const searchTerm = searchInput.value.toLowerCase();
      const locationValue = locationFilter.value.toLowerCase();
      const typeValue = typeFilter.value.toLowerCase();
      const salaryMin = salaryMinInput ? salaryMinInput.value : '';
      const salaryMax = salaryMaxInput ? salaryMaxInput.value : '';
      const experienceValue = experienceFilter ? experienceFilter.value : '';
      const skillsValue = skillsFilter ? skillsFilter.value.toLowerCase() : '';

      jobBoxes.forEach(box => {
         const title = box.querySelector('.job-title').textContent.toLowerCase();
         const company = box.querySelector('.company h3').textContent.toLowerCase();
         const location = box.querySelector('.location span').textContent.toLowerCase();
         const type = box.querySelector('.tags p:nth-child(2) span').textContent.toLowerCase();
         const salary = box.querySelector('.tags p:nth-child(1) span').textContent.toLowerCase();

         const matchesSearch = !searchTerm || title.includes(searchTerm) || company.includes(searchTerm) || location.includes(searchTerm);
         const matchesLocation = !locationValue || location.includes(locationValue);
         const matchesType = !typeValue || type.includes(typeValue);
         const matchesSalaryMin = !salaryMin || salary.includes(salaryMin);
         const matchesSalaryMax = !salaryMax || salary.includes(salaryMax);
         const matchesExperience = !experienceValue; // Simplified, as experience isn't in the job display
         const matchesSkills = !skillsValue; // Simplified, as skills aren't in the job display

         if (matchesSearch && matchesLocation && matchesType && matchesSalaryMin && matchesSalaryMax && matchesExperience && matchesSkills) {
            box.style.display = 'block';
            box.style.animation = 'fadeInUp 0.5s ease-out';
         } else {
            box.style.display = 'none';
         }
      });
   }

   // Event listeners
   if (searchBtn) searchBtn.addEventListener('click', filterJobs);
   if (searchInput) {
      searchInput.addEventListener('keyup', function(e) {
         if (e.key === 'Enter') {
            filterJobs();
         }
      });
   }
   if (locationFilter) locationFilter.addEventListener('change', filterJobs);
   if (typeFilter) typeFilter.addEventListener('change', filterJobs);
   if (applyFiltersBtn) applyFiltersBtn.addEventListener('click', filterJobs);

   if (clearFiltersBtn) {
      clearFiltersBtn.addEventListener('click', function() {
         if (searchInput) searchInput.value = '';
         if (locationFilter) locationFilter.value = '';
         if (typeFilter) typeFilter.value = '';
         if (salaryMinInput) salaryMinInput.value = '';
         if (salaryMaxInput) salaryMaxInput.value = '';
         if (experienceFilter) experienceFilter.value = '';
         if (skillsFilter) skillsFilter.value = '';
         jobBoxes.forEach(box => {
            box.style.display = 'block';
            box.style.animation = 'fadeInUp 0.5s ease-out';
         });
      });
   }
});

// Form Validation
document.addEventListener('DOMContentLoaded', function() {
   // Contact Form Validation
   const contactForm = document.querySelector('#contact form');
   if (contactForm) {
      contactForm.addEventListener('submit', function(e) {
         e.preventDefault();
         const name = contactForm.querySelector('input[name="name"]');
         const email = contactForm.querySelector('input[name="email"]');
         const number = contactForm.querySelector('input[name="number"]');
         const message = contactForm.querySelector('textarea[name="message"]');

         let isValid = true;

         // Name validation
         if (name.value.trim().length < 2) {
            showError(name, 'Name must be at least 2 characters');
            isValid = false;
         } else {
            clearError(name);
         }

         // Email validation
         const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
         if (!emailRegex.test(email.value)) {
            showError(email, 'Please enter a valid email');
            isValid = false;
         } else {
            clearError(email);
         }

         // Phone validation
         if (number.value.length < 10) {
            showError(number, 'Phone number must be at least 10 digits');
            isValid = false;
         } else {
            clearError(number);
         }

         // Message validation
         if (message.value.trim().length < 10) {
            showError(message, 'Message must be at least 10 characters');
            isValid = false;
         } else {
            clearError(message);
         }

         if (isValid) {
            showSuccess('Message sent successfully!');
            contactForm.reset();
         }
      });
   }

   // Login Form Validation
   const loginForm = document.querySelector('#login form');
   if (loginForm) {
      loginForm.addEventListener('submit', function(e) {
         e.preventDefault();
         const email = loginForm.querySelector('input[name="email"]');
         const password = loginForm.querySelector('input[name="pass"]');

         let isValid = true;

         if (!email.value) {
            showError(email, 'Email is required');
            isValid = false;
         } else {
            clearError(email);
         }

         if (password.value.length < 6) {
            showError(password, 'Password must be at least 6 characters');
            isValid = false;
         } else {
            clearError(password);
         }

         if (isValid) {
            showSuccess('Login successful!');
            // Simulate login
            setTimeout(() => {
               window.location.href = 'home.html';
            }, 1000);
         }
      });
   }

   // Register Form Validation
   const registerForm = document.querySelector('#register form');
   if (registerForm) {
      registerForm.addEventListener('submit', function(e) {
         e.preventDefault();
         const name = registerForm.querySelector('input[name="name"]');
         const email = registerForm.querySelector('input[name="email"]');
         const password = registerForm.querySelector('input[name="pass"]');
         const confirmPassword = registerForm.querySelector('input[name="c_pass"]');

         let isValid = true;

         if (name.value.trim().length < 2) {
            showError(name, 'Name must be at least 2 characters');
            isValid = false;
         } else {
            clearError(name);
         }

         const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
         if (!emailRegex.test(email.value)) {
            showError(email, 'Please enter a valid email');
            isValid = false;
         } else {
            clearError(email);
         }

         if (password.value.length < 6) {
            showError(password, 'Password must be at least 6 characters');
            isValid = false;
         } else {
            clearError(password);
         }

         if (password.value !== confirmPassword.value) {
            showError(confirmPassword, 'Passwords do not match');
            isValid = false;
         } else {
            clearError(confirmPassword);
         }

         if (isValid) {
            showSuccess('Registration successful!');
            registerForm.reset();
            setTimeout(() => {
               window.location.href = 'login.html';
            }, 1000);
         }
      });
   }

   function showError(input, message) {
      clearError(input);
      const errorDiv = document.createElement('div');
      errorDiv.className = 'error-message';
      errorDiv.textContent = message;
      input.parentNode.appendChild(errorDiv);
      input.style.borderColor = 'red';
   }

   function clearError(input) {
      const existingError = input.parentNode.querySelector('.error-message');
      if (existingError) {
         existingError.remove();
      }
      input.style.borderColor = '';
   }

   function showSuccess(message) {
      const successDiv = document.createElement('div');
      successDiv.className = 'success-message';
      successDiv.textContent = message;
      successDiv.style.cssText = `
         position: fixed;
         top: 20px;
         right: 20px;
         background: var(--accent);
         color: white;
         padding: 1rem 2rem;
         border-radius: var(--radius);
         z-index: 10000;
         animation: slideInRight 0.3s ease-out;
      `;
      document.body.appendChild(successDiv);
      setTimeout(() => {
         successDiv.remove();
      }, 3000);
   }
});

// Job Save/Unsave System
document.addEventListener('DOMContentLoaded', function() {
   const saveButtons = document.querySelectorAll('.save-job-btn');

   saveButtons.forEach(button => {
      button.addEventListener('click', function() {
         const jobId = this.getAttribute('data-job-id');
         const isSaved = this.textContent.trim().includes('Saved');

         fetch(`/api/save-job/${jobId}`, {
            method: 'POST',
            headers: {
               'Content-Type': 'application/json',
            }
         })
         .then(response => response.json())
         .then(data => {
            if (data.success) {
               if (data.saved) {
                  this.innerHTML = '<i class="fas fa-heart"></i> Saved';
                  this.classList.add('saved');
                  showNotification('Job saved successfully!', 'success');
               } else {
                  this.innerHTML = '<i class="fas fa-heart"></i> Save';
                  this.classList.remove('saved');
                  showNotification('Job removed from saved jobs!', 'info');
               }
            } else {
               showNotification(data.message, 'error');
            }
         })
         .catch(error => {
            console.error('Error:', error);
            showNotification('An error occurred while saving the job.', 'error');
         });
      });
   });
});

// Dark Mode Toggle
document.addEventListener('DOMContentLoaded', function() {
   // Create dark mode toggle button
   const darkModeToggle = document.createElement('button');
   darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>';
   darkModeToggle.className = 'dark-mode-toggle';
   darkModeToggle.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background: var(--primary);
      color: white;
      border: none;
      cursor: pointer;
      z-index: 1000;
      box-shadow: var(--shadow);
      transition: var(--transition);
   `;
   document.body.appendChild(darkModeToggle);

   // Load dark mode preference
   const isDarkMode = localStorage.getItem('darkMode') === 'true';
   if (isDarkMode) {
      document.body.classList.add('dark-mode');
      darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
   }

   // Toggle dark mode
   darkModeToggle.addEventListener('click', function() {
      document.body.classList.toggle('dark-mode');
      const isDark = document.body.classList.contains('dark-mode');
      localStorage.setItem('darkMode', isDark);
      this.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
      showNotification(isDark ? 'Dark mode enabled!' : 'Light mode enabled!', 'info');
   });
});

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
   anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
         target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
         });
      }
   });
});

// Notification system
function showNotification(message, type = 'info') {
   const notification = document.createElement('div');
   notification.className = `notification ${type}`;
   notification.textContent = message;
   notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: ${type === 'success' ? 'var(--accent)' : type === 'error' ? '#dc3545' : 'var(--primary)'};
      color: white;
      padding: 1rem 2rem;
      border-radius: var(--radius);
      z-index: 10000;
      animation: slideInRight 0.3s ease-out;
      margin-top: ${document.querySelectorAll('.notification').length * 60}px;
   `;
   document.body.appendChild(notification);
   setTimeout(() => {
      notification.remove();
   }, 3000);
}

// Add loading animation for forms
document.querySelectorAll('form').forEach(form => {
   form.addEventListener('submit', function(e) {
      const submitBtn = this.querySelector('input[type="submit"]');
      if (submitBtn) {
         submitBtn.value = 'Processing...';
         submitBtn.disabled = true;
      }
   });
});

// Enhanced interactivity for login and register pages
document.addEventListener('DOMContentLoaded', function() {
   // Password strength indicator
   const passwordInputs = document.querySelectorAll('input[name="pass"], input[name="c_pass"]');
   passwordInputs.forEach(input => {
      const strengthIndicator = document.createElement('div');
      strengthIndicator.className = 'password-strength';
      strengthIndicator.style.cssText = `
         margin-top: 0.5rem;
         height: 4px;
         background: #e9ecef;
         border-radius: 2px;
         overflow: hidden;
      `;
      input.parentNode.appendChild(strengthIndicator);

      const strengthBar = document.createElement('div');
      strengthBar.style.cssText = `
         height: 100%;
         width: 0%;
         transition: width 0.3s ease, background-color 0.3s ease;
      `;
      strengthIndicator.appendChild(strengthBar);

      input.addEventListener('input', function() {
         const strength = calculatePasswordStrength(this.value);
         strengthBar.style.width = strength.percentage + '%';
         strengthBar.style.backgroundColor = strength.color;
      });
   });

   function calculatePasswordStrength(password) {
      let score = 0;
      if (password.length >= 8) score += 25;
      if (/[a-z]/.test(password)) score += 25;
      if (/[A-Z]/.test(password)) score += 25;
      if (/[0-9]/.test(password)) score += 15;
      if (/[^A-Za-z0-9]/.test(password)) score += 10;

      let color = '#dc3545'; // red
      if (score >= 50) color = '#ffc107'; // yellow
      if (score >= 75) color = '#28a745'; // green

      return { percentage: score, color: color };
   }

   // Eye icon for password visibility toggle
   const passwordFields = document.querySelectorAll('input[type="password"]');
   passwordFields.forEach(field => {
      const toggleBtn = document.createElement('button');
      toggleBtn.type = 'button';
      toggleBtn.className = 'password-toggle';
      toggleBtn.innerHTML = '<i class="fas fa-eye"></i>';
      toggleBtn.style.cssText = `
         position: absolute;
         right: 15px;
         top: 50%;
         transform: translateY(-50%);
         background: none;
         border: none;
         color: var(--primary);
         cursor: pointer;
         font-size: 1.6rem;
         z-index: 2;
      `;
      field.parentNode.style.position = 'relative';
      field.parentNode.appendChild(toggleBtn);

      toggleBtn.addEventListener('click', function() {
         const type = field.getAttribute('type') === 'password' ? 'text' : 'password';
         field.setAttribute('type', type);
         this.innerHTML = type === 'password' ? '<i class="fas fa-eye"></i>' : '<i class="fas fa-eye-slash"></i>';
      });
   });

   // Floating label effect removed - labels are no longer used

   // Typing animation for branding text
   const brandingText = document.querySelector('.branding-content p');
   if (brandingText) {
      const text = brandingText.textContent;
      brandingText.textContent = '';
      let i = 0;
      const typeWriter = () => {
         if (i < text.length) {
            brandingText.textContent += text.charAt(i);
            i++;
            setTimeout(typeWriter, 50);
         }
      };
      setTimeout(typeWriter, 1000);
   }

   // Particle animation background
   const canvas = document.createElement('canvas');
   canvas.id = 'particle-canvas';
   canvas.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 0;
   `;
   document.body.appendChild(canvas);

   const ctx = canvas.getContext('2d');
   let particles = [];

   function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
   }

   function createParticles() {
      particles = [];
      for (let i = 0; i < 50; i++) {
         particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
            size: Math.random() * 2 + 1,
            opacity: Math.random() * 0.5 + 0.2
         });
      }
   }

   function animateParticles() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      particles.forEach(particle => {
         particle.x += particle.vx;
         particle.y += particle.vy;

         // Add some wave motion
         particle.y += Math.sin(Date.now() * 0.001 + particle.x * 0.01) * 0.5;

         if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1;
         if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1;

         // Dynamic opacity based on position
         const centerX = canvas.width / 2;
         const centerY = canvas.height / 2;
         const distance = Math.sqrt(Math.pow(particle.x - centerX, 2) + Math.pow(particle.y - centerY, 2));
         const maxDistance = Math.sqrt(Math.pow(centerX, 2) + Math.pow(centerY, 2));
         particle.opacity = (1 - distance / maxDistance) * 0.6 + 0.1;

         ctx.beginPath();
         ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
         ctx.fillStyle = `rgba(255, 255, 255, ${particle.opacity})`;
         ctx.fill();

         // Add glow effect
         ctx.shadowBlur = 10;
         ctx.shadowColor = 'rgba(255, 255, 255, 0.5)';
         ctx.fill();
         ctx.shadowBlur = 0;
      });

      requestAnimationFrame(animateParticles);
   }

   window.addEventListener('resize', resizeCanvas);
   resizeCanvas();
   createParticles();
   animateParticles();

   // Enhanced form submission with loading states and ripple effects
   const accountForms = document.querySelectorAll('.account-form form');
   accountForms.forEach(form => {
      form.addEventListener('submit', function(e) {
         const submitBtn = this.querySelector('input[type="submit"]');
         if (submitBtn) {
            submitBtn.style.transform = 'scale(0.95)';
            submitBtn.value = 'Processing...';

            // Add loading spinner with enhanced animation
            const spinner = document.createElement('i');
            spinner.className = 'fas fa-spinner fa-spin';
            spinner.style.cssText = `
               margin-left: 10px;
               animation: spin 1s linear infinite;
               filter: drop-shadow(0 0 5px rgba(255,255,255,0.5));
            `;
            submitBtn.parentNode.appendChild(spinner);

            // Add ripple effect on form
            const ripple = document.createElement('div');
            ripple.style.cssText = `
               position: absolute;
               top: 50%;
               left: 50%;
               width: 0;
               height: 0;
               border-radius: 50%;
               background: rgba(255,255,255,0.3);
               transform: translate(-50%, -50%);
               animation: rippleExpand 0.6s ease-out;
               pointer-events: none;
               z-index: 10;
            `;
            submitBtn.style.position = 'relative';
            submitBtn.appendChild(ripple);

            // Simulate processing time
            setTimeout(() => {
               submitBtn.style.transform = 'scale(1)';
               submitBtn.value = submitBtn.getAttribute('data-original-value') || 'Submit';
               if (spinner.parentNode) {
                  spinner.parentNode.removeChild(spinner);
               }
               if (ripple.parentNode) {
                  ripple.parentNode.removeChild(ripple);
               }
            }, 2000);
         }
      });
   });

   // Add ripple effect to buttons on click
   document.addEventListener('click', function(e) {
      if (e.target.classList.contains('btn') || e.target.type === 'submit') {
         const button = e.target;
         const ripple = document.createElement('span');
         const rect = button.getBoundingClientRect();
         const size = Math.max(rect.width, rect.height);
         const x = e.clientX - rect.left - size / 2;
         const y = e.clientY - rect.top - size / 2;

         ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255,255,255,0.4);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s ease-out;
            pointer-events: none;
         `;

         button.style.position = 'relative';
         button.style.overflow = 'hidden';
         button.appendChild(ripple);

         setTimeout(() => {
            ripple.remove();
         }, 600);
      }
   });

   // Parallax effect for branding section
   let parallaxElements = document.querySelectorAll('.branding-content h1, .branding-content p, .feature-item');
   window.addEventListener('scroll', function() {
      const scrolled = window.pageYOffset;
      const rate = scrolled * -0.5;

      parallaxElements.forEach(element => {
         element.style.transform = `translateY(${rate * 0.1}px)`;
      });
   });

   // Save original button values
   document.querySelectorAll('input[type="submit"]').forEach(btn => {
      btn.setAttribute('data-original-value', btn.value);
   });
});
