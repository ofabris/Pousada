function formatarData(data) {
    const dataObj = new Date(data);
    dataObj.setDate(dataObj.getDate() + 1); // Adiciona 1 dia à data para corrigir o problema
    const dia = String(dataObj.getDate()).padStart(2, '0');
    const mes = String(dataObj.getMonth() + 1).padStart(2, '0');
    const ano = dataObj.getFullYear();
    return `${dia}/${mes}/${ano}`;
}

document.addEventListener("DOMContentLoaded", function () {
    const buscarReservasBtn = document.getElementById('buscarReservasBtn');
    const cpfInput = document.getElementById('cpfInput');
    const reservasContainer = document.getElementById('reservasContainer');

    buscarReservasBtn.addEventListener('click', function () {
        const cpf = cpfInput.value;

        if (!cpf) {
            alert('Por favor, digite um CPF.');
            return;
        }

        fetch(`http://localhost:8083/reservas?cpf=${cpf}`)
            .then(response => response.json())
            .then(data => {
                // Limpar o conteúdo anterior
                reservasContainer.innerHTML = '';

                if (data.error) {
                    alert(data.error);
                } else if (data.length === 0) {
                    reservasContainer.innerHTML = '<p>Nenhuma reserva encontrada para este CPF.</p>';
                } else {
                    data.forEach(reserva => {
                        const card = document.createElement('div');
                        card.className = 'card mt-3';
                        card.innerHTML = `
                        <div class="card-body">
                            <h5 class="card-title"><strong>Dados da Reserva</strong></h5>
                            <p class="card-text"><strong>Data de entrada:</strong> ${formatarData(reserva.DT_INI_RESERVA)}</p>
                            <p class="card-text"><strong>Data de saída:</strong> ${formatarData(reserva.DT_FIM_RESERVA)}</p>
                            <p class="card-text"><strong>Quarto:</strong> ${reserva.DESC_QUARTO}</p>
                            <button class="btn btn-danger btn-excluir" data-reserva-id="${reserva.ID}">Excluir</button>
                        </div>`;
                        reservasContainer.appendChild(card);
                    });
                }
            })
            .catch(error => {
                console.error('Erro ao buscar as reservas:', error);
                alert('Erro ao buscar as reservas. Por favor, tente novamente.');
            });
    });

    // Adicionando evento de clique para os botões de exclusão
    reservasContainer.addEventListener('click', function (event) {
        if (event.target.classList.contains('btn-excluir')) {
            const reservaId = event.target.dataset.reservaId;
            // Aqui você pode chamar uma função para excluir a reserva com o ID fornecido
            excluirReserva(reservaId);
        }
    });

    function excluirReserva(reservaId) {
        fetch(`http://localhost:8083/excluir_reserva/${reservaId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao excluir a reserva.');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            // Atualize as reservas após a exclusão
            buscarReservasBtn.click();
        })
        .catch(error => {
            console.error('Erro ao excluir a reserva:', error);
            alert('Erro ao excluir a reserva. Por favor, tente novamente.');
        });
    }
});
