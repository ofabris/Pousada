document.getElementById('cadastroForm').addEventListener('submit', function (event) {
  event.preventDefault();

  const nome = document.getElementById('nome').value;
  const telefone = document.getElementById('telefone').value;
  const cpf = document.getElementById('cpf').value;
  const dataNascimento = document.getElementById('dataNascimento').value;
  const senha = document.getElementById('senha').value; // Novo campo de senha

  if (nome.trim() === '' || telefone.trim() === '' || cpf.trim() === '' || dataNascimento.trim() === '' || senha.trim() === '') {
    alert('Por favor, preencha todos os campos.');
    return;
  }

  // Dados a serem enviados para a API
  const formData = {
    nome: nome,
    telefone: telefone,
    cpf: cpf,
    dataNascimento: dataNascimento,
    senha: senha
  };

  // Faz uma solicitação para a API em Python para realizar o cadastro do usuário
  fetch('http://localhost:8080/cadastrar', {
    method: 'POST', // Método da solicitação HTTP
    headers: {
      'Content-Type': 'application/json' // Tipo de conteúdo da solicitação
    },
    body: JSON.stringify(formData) // Converte os dados do formulário para JSON
  })
    .then(response => {
      if (response.ok) {
        // Se a resposta for bem-sucedida, exibe uma mensagem de sucesso
        alert('Cadastro realizado com sucesso!');
        document.getElementById('cadastroForm').reset(); // Limpa o formulário
        window.location.href = '../../pages/login/index.html'; // Redireciona para a página de login
      } else {
        // Se a resposta não for bem-sucedida, exibe um alerta com o erro
        return response.json().then(data => {
          throw new Error(data.message);
        });
      }
    })
    .catch(error => {
      // Captura e trata quaisquer erros que ocorram durante a solicitação
      console.error('Erro ao realizar cadastro:', error);
      alert('Erro ao realizar cadastro: ' + error.message);
    });
});