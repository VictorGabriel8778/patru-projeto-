async function carregarProdutos() {
    let resposta = await fetch('/produtos');
    let produtos = await resposta.json();
    let tabela = document.getElementById("tabela-produtos");
    tabela.innerHTML = "";

    produtos.forEach(produto => {
        let linha = document.createElement("tr");
        linha.innerHTML = `
            <td>${produto[1]}</td>
            <td>${produto[2]}</td>
            <td>R$ ${produto[3]}</td>
            <td>
                <button class="btn-editar" onclick="editarProduto(${produto[0]})">✏️</button>
                <button class="btn-remover" onclick="removerProduto(${produto[0]})">🗑️</button>
            </td>
        `;
        tabela.appendChild(linha);
    });
}

async function adicionarProduto() {
    let nome = document.getElementById("nome").value;
    let quantidade = document.getElementById("quantidade").value;
    let preco = document.getElementById("preco").value;

    if (!nome || quantidade <= 0 || preco <= 0) {
        alert("Preencha os campos corretamente!");
        return;
    }

    await fetch('/api/adicionar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome, quantidade, preco })
    });

    fecharPopup();
    carregarProdutos();
}

async function removerProduto(id) {
    if (confirm("Tem certeza que deseja remover este produto?")) {
        await fetch(`/remover/${id}`, { method: 'DELETE' });
        carregarProdutos();
    }
}

function abrirPopup() {
    document.getElementById("popup").style.display = "block";
}

function fecharPopup() {
    document.getElementById("popup").style.display = "none";
}
