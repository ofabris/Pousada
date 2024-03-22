document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('loginForm').addEventListener('submit', function (event) {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        fetch('http://localhost:8080/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: username, password: password })
        })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Nome de usuário ou senha incorretos');
                }
            })
            .then(data => {
                if (data.success) {
                    window.location.href = '../../pages/home/home.html';
                } else {
                    alert('Nome de usuário ou senha incorretos. Por favor, tente novamente.');
                }
            })
            .catch(error => {
                console.error('Erro ao fazer solicitação:', error);
                alert(error.message);
            });
    });
});
