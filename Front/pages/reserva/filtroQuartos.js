document.addEventListener("DOMContentLoaded", function() {
    const btnFiltrar = document.getElementById('btnFiltrar');

    btnFiltrar.addEventListener('click', function() {
        const dataEntrada = document.getElementById('dataEntrada').value;
        const dataSaida = document.getElementById('dataSaida').value;

        // Verificar se as datas de entrada e saída foram fornecidas
        if (!dataEntrada || !dataSaida) {
            alert('Por favor, informe a data de entrada e saída.');
            return;
        }

        // Fazer solicitação para a API Flask com as datas de entrada e saída
        fetch(`http://localhost:8082/quartos?dataEntrada=${dataEntrada}&dataSaida=${dataSaida}`)
            .then(response => response.json())
            .then(data => {
                const dropdown = document.getElementById('quarto');

                // Limpar as opções atuais do dropdown
                dropdown.innerHTML = '';

                // Preencher o dropdown com os dados retornados pela API
                data.forEach(quarto => {
                    const option = document.createElement('option');
                    option.value = quarto;
                    option.textContent = quarto;
                    dropdown.appendChild(option);
                });
            })
            .catch(error => {
                alert('Erro ao filtrar os quartos', error);
            });
    });
});
