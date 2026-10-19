# GeoLease

Projeto acadêmico de análise geográfica de imóveis utilizando **DBSCAN**, desenvolvido com Python, FastAPI, PostgreSQL e PostGIS.

## Objetivo

Consultar imóveis que possuem coordenadas geográficas e agrupá-los de acordo com a proximidade espacial. O algoritmo DBSCAN utiliza a distância Haversine para trabalhar com coordenadas geográficas.

> **Observação:** os resultados demonstrados até o momento usam dados sintéticos para validar o funcionamento básico. Eles não representam uma avaliação com dados reais.

## Tecnologias

- Python
- FastAPI e Uvicorn — API HTTP
- PostgreSQL e PostGIS — armazenamento de dados espaciais
- SQLAlchemy e Psycopg — conexão com o banco
- Pandas e NumPy — organização e preparação das coordenadas
- scikit-learn — implementação do DBSCAN
- HTML, CSS e JavaScript — interface web

## Estrutura do repositório

```text
geolease/
├── Backend/
│   ├── database.py
│   ├── dbscan.py
│   ├── main.py
│   ├── requirements.txt
│   ├── test_db.py
│   └── test_imoveis.py
├── Frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
└── .gitignore
```

### Backend

- **`main.py`**: cria a API FastAPI e disponibiliza as rotas `/`, `/imoveis` e `/dbscan`. Consulta os imóveis no banco, prepara as coordenadas, executa o DBSCAN e devolve os grupos e as estatísticas em JSON.
- **`database.py`**: lê as configurações locais do arquivo `.env` e cria o mecanismo de conexão com PostgreSQL usando SQLAlchemy e Psycopg.
- **`dbscan.py`**: executa o algoritmo diretamente pelo terminal, consultando os imóveis e imprimindo a classificação de cada um, a quantidade de grupos e a quantidade de ruídos.
- **`test_db.py`**: verifica a conexão com o banco e consulta a versão do PostGIS.
- **`test_imoveis.py`**: script auxiliar relacionado à consulta/teste de imóveis.
- **`requirements.txt`**: lista as bibliotecas Python necessárias.

### Frontend

- **`index.html`**: define a estrutura do painel, os indicadores, a tabela de imóveis, o filtro por grupo e o botão de análise.
- **`script.js`**: comunica-se com a API, carrega os imóveis, executa a análise, atualiza os indicadores e filtra a tabela.
- **`style.css`**: define o visual do painel e seu comportamento em telas menores.

## Como o DBSCAN é aplicado

O projeto utiliza os seguintes parâmetros:

- **`eps = 5 km`**: distância máxima considerada para a vizinhança.
- **`min_samples = 2`**: quantidade mínima de pontos na vizinhança para formar uma região densa, incluindo o próprio ponto.
- **Métrica: `haversine`**: calcula a distância angular entre coordenadas geográficas.
- **Raio médio da Terra: `6371.0088 km`**.

Como a métrica Haversine espera coordenadas em radianos, latitude e longitude são convertidas de graus para radianos. O parâmetro `eps` também é convertido de quilômetros para radianos dividindo-se o raio em quilômetros pelo raio médio da Terra.

O DBSCAN atribui um rótulo a cada imóvel. Os rótulos não negativos identificam grupos; o rótulo `-1` indica um ponto classificado como ruído.

## Pré-requisitos

1. Python instalado.
2. PostgreSQL instalado com a extensão PostGIS habilitada.
3. Banco de dados configurado com a tabela `public.imoveis`, contendo pelo menos `id`, `nome`, `parque`, `area_ha` e `geom`. A coluna `geom` deve armazenar pontos geográficos compatíveis com SRID 4326.
4. Arquivo local `Backend/.env` com as credenciais do banco.

Exemplo de configuração para `Backend/.env`:

```env
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=geolase
```

Use suas próprias credenciais. **Não publique o arquivo `.env` nem senhas no repositório.**

## Como executar

Abra um terminal na pasta `Backend`:

```powershell
cd Backend
python -m venv .venv
..venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python test_db.py
```

Se o teste de conexão for concluído com sucesso, inicie a API:

```powershell
uvicorn main:app --reload
```

A API ficará disponível em http://127.0.0.1:8000. A documentação interativa do FastAPI fica em http://127.0.0.1:8000/docs.

Para abrir a interface, utilize uma extensão como **Live Server** no VS Code e abra `Frontend/index.html` usando a porta 5500. O backend permite essa origem no CORS.

## Rotas da API

| Método | Rota | Função |
|---|---|---|
| GET | `/` | Verifica se a API está funcionando. |
| GET | `/imoveis` | Retorna os imóveis com coordenadas disponíveis. |
| GET | `/dbscan` | Executa o DBSCAN e retorna os imóveis classificados, parâmetros e estatísticas. |

## Resultado de teste conhecido

Em um teste com **seis imóveis sintéticos**, o algoritmo identificou **dois grupos de três imóveis e nenhum ponto de ruído**, utilizando `eps = 5 km` e `min_samples = 2`. Esse resultado confirma o comportamento observado nesse conjunto de teste, mas não garante a mesma distribuição com outros dados ou parâmetros.

## Limitações atuais

- O resultado depende dos dados e das coordenadas presentes no banco.
- O repositório não inclui um script de criação/população completa do banco; é necessário configurar previamente o esquema e os dados.
- A interface apresenta os imóveis em uma tabela e mostra os agrupamentos; ela não é um mapa geográfico interativo.
- Os parâmetros do DBSCAN estão definidos no código e não são configurados pela interface.

## Contexto acadêmico

Projeto desenvolvido para a disciplina de Programação Avançada, com foco na implementação e demonstração do algoritmo de agrupamento espacial DBSCAN.
