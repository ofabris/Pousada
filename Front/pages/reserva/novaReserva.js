document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector('form');

    // Adicionar um evento de escuta para o envio do formulário
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const dataEntrada = document.getElementById('dataEntrada').value;
        const dataSaida = document.getElementById('dataSaida').value;
        const quarto = document.getElementById('quarto').value;
        const cpf = document.getElementById('cpf').value;

        const dadosReserva = {
            quarto: quarto,
            dataEntrada: dataEntrada,
            dataSaida: dataSaida,
            cpf: cpf
        };

        fetch('http://localhost:8082/quartos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dadosReserva)
        })
            .then(response => {
                if (response.ok) {
                    // Limpar o formulário
                    form.reset();
                    // Mostrar mensagem de sucesso
                    alert('Reserva cadastrada com sucesso!');
                } else {
                    throw new Error('Erro ao realizar a reserva');
                }
            })
            .catch(error => {
                console.error('Erro ao cadastrar a reserva:', error);
            });
    });
});
