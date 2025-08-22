const token = localStorage.getItem('accessToken');
if (!token) {
    alert('Acesso negado. Por favor, faça o login primeiro.');
    window.location.href = 'index.html';
} else {
    document.body.style.visibility = 'visible';
}

const authHeaders = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
};

const API_URL = 'http://127.0.0.1:8000';

const projetoForm = document.getElementById('projetoForm');
const projetosTbody = document.getElementById('projetosTbody');
const projetoIdInput = document.getElementById('projetoId');
const nomeInput = document.getElementById('nome');
const descricaoInput = document.getElementById('descricao');
const statusInput = document.getElementById('status');
const projetoTabela = document.getElementById('projetosTabela');
const cancelarButton = document.getElementById('cancelarButton');

function listarProjetos() {
    fetch(`${API_URL}/projetos/all_projects`)
        .then(response => response.json())
        .then(projetos => {
            projetosTbody.innerHTML = '';
            projetos.forEach(projeto => {
                const add = document.createElement('tr');
                
                add.innerHTML = `
                    <td>${projeto.id}</td>
                    <td>${projeto.name}</td>
                    <td>${projeto.description}</td>
                    <td>${projeto.status}</td>
                    <td>
                        <button class="editarButton" onclick="prepararEdicao(${projeto.id})">Editar</button>
                        <button class="deletarButton" onclick="deletarProjeto(${projeto.id})">Excluir</button>
                    </td>
                `;
                projetosTbody.appendChild(add);
            });
        })
        .catch(error => {
            console.error("Ocorreu um erro ao listar os projetos:", error);
        });
}

function deletarProjeto (id) {
    if (confirm(`Tem certeza que deseja excluir o projeto id: ${id}?`)) {
        fetch(`${API_URL}/projetos/projects/${id}`, {
            method: 'DELETE'
        })
        .then (response => {
            if (!response.ok) {
                alert('Ocorreu um erro ao excluir o projeto!');
            }
            alert('Projeto excluído com sucesso!');
            listarProjetos();
        })
    }
}

function prepararEdicao(id) {
    fetch(`${API_URL}/projetos/projects/${id}`)
        .then(response => {
            return response.json();
        })
        .then(projeto => {
            projetoIdInput.value = projeto.id;
            nomeInput.value = projeto.name;
            descricaoInput.value = projeto.description; 
            statusInput.value = projeto.status;

            cancelarButton.classList.remove('hidden');
        })
        .catch(error => {
            alert('Não foi possível carregar os dados para edição.');
        });
}


function resetarFormulario () {
    projetoForm.reset();
    projetoIdInput.value = '';
    cancelarButton.classList.add('hidden')
}

projetoForm.addEventListener('submit', function(evento) {
    evento.preventDefault();

    const infoProjetos = {
        name: nomeInput.value,
        description: descricaoInput.value,
        status: statusInput.value
    }

    const idProjeto = projetoIdInput.value
    let url_metodo = `${API_URL}/projetos/create_projects`;
    let metodo = 'POST';

    if (idProjeto) {
        url_metodo = `${API_URL}/projetos/edit_project/${idProjeto}`
        metodo = 'PUT';
    }

    fetch(url_metodo, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(infoProjetos)
    })
    .then(response => {
        if (!response.ok) {
            alert("A requisição falhou!") 
            return response.json();
        }
    })
    .then(() => {
        alert('Requisição concluída!')
        resetarFormulario();
        listarProjetos();
    });
});

cancelarButton.addEventListener('click', resetarFormulario)

listarProjetos();