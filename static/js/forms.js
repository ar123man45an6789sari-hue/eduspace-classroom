document.addEventListener('DOMContentLoaded', () => {
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    const inputs = form.querySelectorAll('input:not([type=hidden]):not([type=radio]):not([type=checkbox]), textarea, select');
    inputs.forEach(input => {
      input.addEventListener('blur', () => validateField(input));
      input.addEventListener('input', () => {
        if (input.classList.contains('is-invalid')) validateField(input);
      });
    });
    
    form.addEventListener('submit', (e) => {
      const btn = form.querySelector('button[type=submit]');
      if (btn && !btn.disabled) {
        btn.disabled = true;
        btn.dataset.originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        setTimeout(() => {
          if (btn.disabled) {
            btn.disabled = false;
            btn.innerHTML = btn.dataset.originalText;
          }
        }, 10000);
      }
    });
  });
});

function validateField(input) {
  const errorDiv = input.parentElement.querySelector('.field-error') || document.createElement('div');
  errorDiv.className = 'field-error';
  
  if (input.hasAttribute('required') && !input.value.trim()) {
    input.classList.add('is-invalid');
    errorDiv.textContent = 'This field is required';
    if (!input.parentElement.contains(errorDiv)) input.parentElement.appendChild(errorDiv);
    return false;
  }
  
  if (input.type === 'email' && input.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value)) {
    input.classList.add('is-invalid');
    errorDiv.textContent = 'Please enter a valid email';
    if (!input.parentElement.contains(errorDiv)) input.parentElement.appendChild(errorDiv);
    return false;
  }
  
  input.classList.remove('is-invalid');
  errorDiv.remove();
  return true;
}
