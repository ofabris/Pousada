document.getElementById('cadastroQuartoForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const descricao = document.getElementById('descricao').value;
    const valor = document.getElementById('valorQuarto').value;

    if (descricao.trim() === '' || valor.trim() === '') {
        alert('Por favor, preencha todos os campos.');
        return;
    }

    const formData = {
        descricao: descricao,
        valor: valor
    };

    fetch('http://localhost:8081/cadastrar_quarto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
        .then(response => {
            if (response.ok) {
                alert('Cadastro realizado com sucesso!');
                document.getElementById('cadastroQuartoForm').reset();
            } else {
                return response.json().then(data => {
                    throw new Error(data.message);
                });
            }
        })
        .catch(error => {
            console.error('Erro ao realizar cadastro:', error);
            alert('Erro ao realizar cadastro: ' + error.message);
        });
});