
const API_URL = "http://127.0.0.1:8000";

const statusApi = document.getElementById("status-api");
const totalImoveis = document.getElementById("total-imoveis");
const totalGrupos = document.getElementById("total-grupos");
const totalRuidos = document.getElementById("total-ruidos");
const tabelaImoveis = document.getElementById("tabela-imoveis");
const filtroGrupo = document.getElementById("filtro-grupo");
const botaoAnalisar = document.getElementById("btn-analisar");
const mensagem = document.getElementById("mensagem");

let imoveis = [];

async function verificarAPI() {
    try {
        const resposta = await fetch(`${API_URL}/`);

        if (!resposta.ok) {
            throw new Error("A API respondeu com erro.");
        }

        statusApi.textContent = "API conectada";
        statusApi.className = "status online";
    } catch (erro) {
        statusApi.textContent = "API desconectada";
        statusApi.className = "status offline";
        mensagem.textContent =
            "Não foi possível conectar à API. Verifique se o servidor está ligado.";
    }
}

async function carregarImoveis() {
    tabelaImoveis.innerHTML = `
        <tr>
            <td colspan="7">Carregando imóveis...</td>
        </tr>
    `;

    try {
        const resposta = await fetch(`${API_URL}/imoveis`);

        if (!resposta.ok) {
            throw new Error("Erro ao consultar os imóveis.");
        }

        const dados = await resposta.json();
        imoveis = dados.imoveis;

        preencherFiltro();
        exibirImoveis(imoveis);
        totalImoveis.textContent = dados.total;
    } catch (erro) {
        tabelaImoveis.innerHTML = `
            <tr>
                <td colspan="7">Não foi possível carregar os imóveis.</td>
            </tr>
        `;

        mensagem.textContent =
            "Falha ao buscar os imóveis. Verifique se a API está funcionando.";
    }
}

function preencherFiltro() {
    const grupoSelecionado = filtroGrupo.value;
    const grupos = [...new Set(
        imoveis
            .filter(imovel => imovel.grupo !== undefined)
            .map(imovel => imovel.grupo)
    )].sort((a, b) => a - b);

    filtroGrupo.innerHTML =
        '<option value="todos">Todos os grupos</option>';

    grupos.forEach(grupo => {
        const opcao = document.createElement("option");
        opcao.value = String(grupo);
        opcao.textContent = grupo === -1
            ? "Ruído"
            : `Grupo ${grupo}`;

        filtroGrupo.appendChild(opcao);
    });

    if ([...filtroGrupo.options].some(
        opcao => opcao.value === grupoSelecionado
    )) {
        filtroGrupo.value = grupoSelecionado;
    }
}

function exibirImoveis(lista) {
    if (lista.length === 0) {
        tabelaImoveis.innerHTML = `
            <tr>
                <td colspan="7">Nenhum imóvel encontrado.</td>
            </tr>
        `;
        return;
    }

    tabelaImoveis.innerHTML = "";

    lista.forEach(imovel => {
        const linha = document.createElement("tr");

        const grupo = imovel.grupo;
        let classificacao = "Não analisado";
        let classeGrupo = "grupo";

        if (grupo !== undefined) {
            classificacao = grupo === -1
                ? "Ruído"
                : `Grupo ${grupo}`;

            if (grupo === -1) {
                classeGrupo += " ruido";
            }
        }

        const valores = [
            imovel.id,
            imovel.nome,
            imovel.parque,
            `${Number(imovel.area_ha).toFixed(2)} ha`,
            imovel.latitude,
            imovel.longitude
        ];

        valores.forEach(valor => {
            const celula = document.createElement("td");
            celula.textContent = valor ?? "—";
            linha.appendChild(celula);
        });

        const celulaGrupo = document.createElement("td");
        const etiqueta = document.createElement("span");

        etiqueta.className = classeGrupo;
        etiqueta.textContent = classificacao;

        celulaGrupo.appendChild(etiqueta);
        linha.appendChild(celulaGrupo);
        tabelaImoveis.appendChild(linha);
    });
}

async function executarAnalise() {
    botaoAnalisar.disabled = true;
    botaoAnalisar.textContent = "Analisando...";
    mensagem.textContent = "Executando o DBSCAN...";

    try {
        const resposta = await fetch(`${API_URL}/dbscan`);

        if (!resposta.ok) {
            throw new Error("Erro ao executar o DBSCAN.");
        }

        const dados = await resposta.json();

        imoveis = dados.imoveis;

        totalImoveis.textContent = dados.total_imoveis;
        totalGrupos.textContent = dados.total_grupos;
        totalRuidos.textContent = dados.total_ruidos;

        preencherFiltro();
        filtroGrupo.value = "todos";
        exibirImoveis(imoveis);

        mensagem.textContent =
            "Análise concluída com sucesso!";
    } catch (erro) {
        mensagem.textContent =
            "Não foi possível executar a análise. Verifique a API.";
    } finally {
        botaoAnalisar.disabled = false;
        botaoAnalisar.textContent = "Executar análise DBSCAN";
    }
}

filtroGrupo.addEventListener("change", () => {
    const grupoSelecionado = filtroGrupo.value;

    if (grupoSelecionado === "todos") {
        exibirImoveis(imoveis);
    } else {
        exibirImoveis(
            imoveis.filter(
                imovel => String(imovel.grupo) === grupoSelecionado
            )
        );
    }
});

botaoAnalisar.addEventListener("click", executarAnalise);

async function iniciarPainel() {
    await verificarAPI();
    await carregarImoveis();
}

iniciarPainel();
