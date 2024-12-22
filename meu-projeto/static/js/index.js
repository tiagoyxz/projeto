function toggleForm(formType) {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const loginToggle = document.getElementById('login-toggle');
    const registerToggle = document.getElementById('register-toggle');
    
    if (formType === 'login') {
        // Torna o formulário de login visível e o de registro invisível
        loginForm.classList.remove('hidden');
        loginForm.classList.add('visible');
        registerForm.classList.remove('visible');
        registerForm.classList.add('hidden');
        loginToggle.style.backgroundColor = '#d50c2a';
        registerToggle.style.backgroundColor = '#d51936';
    } else {
        // Torna o formulário de registro visível e o de login invisível
        registerForm.classList.remove('hidden');
        registerForm.classList.add('visible');
        loginForm.classList.remove('visible');
        loginForm.classList.add('hidden');
        registerToggle.style.backgroundColor = '#d50c2a';
        loginToggle.style.backgroundColor = '#d51936';
    }
}

// Inicializa com o Login visível
toggleForm('login');

