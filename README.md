#📈 Trading Case API – Backtests com Python
📌 Descrição

Este projeto foi desenvolvido como parte de um processo seletivo.
O objetivo é construir uma API REST em Python para executar backtests de estratégias de trend following (ex.: cruzamento de médias móveis) usando dados históricos do Yahoo Finance e a biblioteca Backtrader.

A API permite que o usuário escolha o ativo, o período e os parâmetros da estratégia, retornando o resultado do backtest em JSON.
O sistema já possui tratamento de erros, validação de entradas e documentação automática.

#⚙️ Tecnologias utilizadas

Python 3.10+

FastAPI – API REST

Backtrader – Backtests

yfinance – Dados históricos

Uvicorn – Servidor ASGI

PostgreSQL – (planejado para persistência futura)

React / JavaScript – Frontend (em pasta separada)

#📂 Estrutura do projeto
trading-case/
├── backend/          # Backend FastAPI
│   ├── main.py
│   ├── requirements.txt
│   └── app/
│       ├── api.py
│       ├── backtest.py
│       └── strategies.py
├── frontend/         # Código do frontend (React ou similar)
├── tests/            # Testes automatizados da API
└── README.md         # Documentação

#🚀 Como rodar o projeto
Backend

Entrar na pasta backend:

cd trading-case/backend


Criar ambiente virtual (opcional, mas recomendado)

python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows


Instalar dependências

pip install -r requirements.txt


Rodar o servidor

uvicorn main:app --reload


A API ficará disponível em: http://127.0.0.1:8000/docs

Frontend

Entrar na pasta frontend

cd trading-case/frontend


Instalar dependências (exemplo com npm ou yarn)

npm install
ou
yarn install


Rodar o frontend

npm start
ou
yarn start

#📡 Endpoints disponíveis
Método	Endpoint	Descrição
POST	/api/backtest	Executa backtests com parâmetros customizados
GET	/api/strategies	Lista estratégias disponíveis
GET	/api/health	Verifica se a API está rodando corretamente

#📊 Exemplo de uso

Request:

curl -X POST http://127.0.0.1:8000/api/backtest \
-H "Content-Type: application/json" \
-d '{"ticker":"AAPL", "start":"2022-01-01", "end":"2023-01-01", "pfast":10, "pslow":30}'


Response:

{
  "ticker": "AAPL",
  "start": "2022-01-01",
  "end": "2023-01-01",
  "initial_cash": 10000.0,
  "final_cash": 10567.34,
  "profit": 567.34
}

#✅ Testes realizados

Rodou múltiplos tickers (AAPL, TSLA, GOOGL) com diferentes parâmetros.

Cobriu entradas inválidas e tratamento de erros.

Todos os endpoints retornaram JSONs com métricas realistas.

Testes automatizados estão na pasta tests/.

#🌟 Próximos passos (diferenciais)

Persistência de resultados em PostgreSQL.

Cron jobs para atualizar indicadores diariamente.

Adição de novas estratégias (Donchian, Momentum, etc.).

Visualização de resultados em gráficos HTML/PDF.

Modelos simples de Machine Learning como filtro de tendência.

Melhor integração com frontend (dashboard interativo).

#👨‍💻 Autor

Desenvolvido por Caio Silva como parte de um desafio técnico.
