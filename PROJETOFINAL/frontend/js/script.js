const API_URL = 'http://127.0.0.1:8000';

const loginFormContainer = document.getElementById('login-form-container');
const registroFormContainer = document.getElementById('registro-form-container');
const linkDeRegistro = document.getElementById('link-de-registro');
const linkDeLogin = document.getElementById('link-de-login');
const loginForm = document.getElementById('login-form');
const registroForm = document.getElementById('registro-form');

loginForm.addEventListener('submit', function(evento) {
    evento.preventDefault();

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded'},
        body: new URLSearchParams({username: email, password: password})
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.detail || 'Email ou senha incorretos.') });
        }
        return response.json();
    })
    .then (data => {
        alert('Login realizado com sucesso!')

        localStorage.setItem('accessToken', data.acess_token);

        window.location.href = 'projetos.html'
    })
    .catch(error => {
        alert(error.message);
    })
});

registroForm.addEventListener('submit', function(evento) {
    evento.preventDefault();

    const email = document.getElementById('registro-email').value;
    const password = document.getElementById('registro-password').value;

    const userData = {
        email: email,
        password: password
    };

    fetch(`${API_URL}/auth/criar_conta`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
    })
    .then(response => {
        if (response.status !== 201) {
            alert("Não foi possível criar a conta.")
        }
        return response.json();
    })
    .then(data => {
        alert(data.mensagem || 'Conta criada com sucesso! Por favor, faça o login.');

        registerFormContainer.classList.add('hidden');
        loginFormContainer.classList.remove('hidden');
    })
    .catch(error => {
        alert(error.message);
    });
});

linkDeRegistro.addEventListener('click', function(evento) {
    evento.preventDefault();
    loginFormContainer.classList.add('hidden');
    registroFormContainer.classList.remove('hidden');
});

linkDeLogin.addEventListener('click', function(evento) {
    evento.preventDefault();
    registroFormContainer.classList.add('hidden');
    loginFormContainer.classList.remove('hidden');
});