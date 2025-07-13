# Simulador de Estratégia de Preço (Análise What-If) para Varejo

Este projeto apresenta um **simulador interativo baseado em Análise What-If** para auxiliar na tomada de decisões estratégicas de precificação em lojas de varejo. Utilizando dados reais de transações comerciais, a ferramenta permite ajustar parâmetros como **margem de lucro** e **elasticidade da demanda**, simulando o impacto dessas variáveis sobre o lucro estimado da loja.

## Funcionalidades principais

- **Modelo simplificado de custo e demanda** baseado em vendas históricas.
- Simulação dinâmica da elasticidade da demanda, com sensibilidade crescente para alterações mais expressivas na margem.
- Visualização interativa com gráficos mensais que comparam o lucro do cenário original com o cenário ajustado.
- Interface amigável e responsiva desenvolvida em Python usando **Streamlit** e **Plotly**.
- Fácil extensão para incorporar novos parâmetros e fontes de dados.

## Benefícios

- Facilita o entendimento do trade-off entre preço, volume e lucro.
- Auxilia gestores na definição de estratégias de precificação mais informadas.
- Possibilita explorar diferentes cenários e prever seus impactos financeiros.

## Tecnologias utilizadas

- Python 3
- Streamlit (dashboard interativo)
- Plotly (visualizações gráficas)
- Pandas (manipulação de dados)

## Como usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git

2. Instale as dependências:
    ```bash
    pip install -r requirements.txt

3. Execute a aplicação:
   ```bash
    streamlit run script.py
    
4. Ajuste os sliders de margem de lucro e elasticidade no painel lateral para explorar diferentes cenários de precificação e visualizar seus impactos no lucro.