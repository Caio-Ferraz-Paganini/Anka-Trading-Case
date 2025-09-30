📈 Trading Case API – Backtests com Python
📌 Descrição

Este projeto foi desenvolvido como parte de um processo seletivo.
O objetivo é construir uma API REST em Python para executar backtests de estratégias de trend following (ex.: cruzamento de médias móveis) usando dados históricos do Yahoo Finance e a biblioteca Backtrader.

A API permite que o usuário escolha o ativo, o período e os parâmetros da estratégia, retornando o resultado do backtest em JSON.

⚙️ Tecnologias utilizadas

Python 3.10+

FastAPI
 – API REST

Backtrader
 – Backtests

yfinance
 – Dados históricos

PostgreSQL
 – (planejado para persistência futura)

🚀 Como rodar o projeto
1. Clonar o repositório
git clone https://github.com/seu-usuario/trading-case.git
cd trading-case

2. Criar ambiente virtual (opcional, mas recomendado)
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

3. Instalar dependências
pip install -r requirements.txt

4. Rodar o servidor
uvicorn main:app --reload


API disponível em: 👉 http://127.0.0.1:8000/docs

📊 Exemplo de uso
Request:
curl -X POST http://127.0.0.1:8000/backtest \
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

🌟 Próximos passos (diferenciais)

Persistir resultados em PostgreSQL.

Criar cron jobs para atualizar indicadores diariamente.

Adicionar novas estratégias (Donchian, Momentum).

Visualização de resultados (gráficos em HTML/PDF).

Modelo simples de Machine Learning como filtro de tendência.

👨‍💻 Autor

Desenvolvido por Caio Silva como parte de um desafio técnico.