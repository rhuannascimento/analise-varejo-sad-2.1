import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# ======================
# CONFIGURAÇÕES INICIAIS
# ======================


@st.cache_data
def load_and_clean_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, encoding="ISO-8859-1")
    df = df.dropna(
        subset=["InvoiceNo", "Description", "Quantity", "InvoiceDate", "UnitPrice"]
    )
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df = df.dropna(subset=["Quantity", "UnitPrice"])
    df = df[df["Quantity"] > 0]
    df = df[df["UnitPrice"] > 0]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df


# ===========================
# PRÉ-PROCESSAMENTO
# ===========================


def aggregate_data(df: pd.DataFrame) -> pd.DataFrame:
    df_grouped = (
        df.groupby("Description")
        .agg({"Quantity": "sum", "UnitPrice": "mean"})
        .reset_index()
    )
    return df_grouped


# ===========================
# SIMULAÇÃO UNIFICADA
# ===========================


def simulate_strategy(
    df: pd.DataFrame, elasticity: float, profit_margin: float
) -> pd.DataFrame:
    df_sim = df.copy()
    df_sim["UnitCost"] = df_sim["UnitPrice"] * (1 - profit_margin)
    df_sim["New Price"] = df_sim["UnitPrice"]
    margin_change = profit_margin - 0.3
    demand_adjustment = 1 - (elasticity * margin_change * (1 + abs(margin_change) * 6))
    df_sim["Adjusted Quantity"] = df_sim["Quantity"] * demand_adjustment
    df_sim["Adjusted Quantity"] = df_sim["Adjusted Quantity"].clip(lower=0)
    df_sim["Estimated Profit"] = (df_sim["New Price"] - df_sim["UnitCost"]) * df_sim[
        "Adjusted Quantity"
    ]
    df_sim["Scenario"] = "Simulado"
    return df_sim


def simulate_baseline(df: pd.DataFrame) -> pd.DataFrame:
    df_base = df.copy()
    df_base["UnitCost"] = df_base["UnitPrice"] * (1 - 0.3)
    df_base["New Price"] = df_base["UnitPrice"]
    df_base["Adjusted Quantity"] = df_base["Quantity"]
    df_base["Estimated Profit"] = (
        df_base["New Price"] - df_base["UnitCost"]
    ) * df_base["Adjusted Quantity"]
    df_base["Scenario"] = "Original"
    return df_base


# ===========================
# DASHBOARD VISUAL
# ===========================


def plot_profit_by_month(df_combined: pd.DataFrame, df_raw: pd.DataFrame):
    df_raw["Month"] = df_raw["InvoiceDate"].dt.to_period("M").astype(str)
    df_summary = df_raw.merge(
        df_combined[["Description", "Scenario", "Estimated Profit"]], on="Description"
    )
    df_monthly = (
        df_summary.groupby(["Month", "Scenario"])["Estimated Profit"]
        .sum()
        .reset_index()
    )
    fig = px.bar(
        df_monthly,
        x="Month",
        y="Estimated Profit",
        color="Scenario",
        barmode="group",
        title="Lucro Mensal Estimado por Cenário",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Total geral
    total_simulado = df_combined[df_combined["Scenario"] == "Simulado"][
        "Estimated Profit"
    ].sum()
    total_original = df_combined[df_combined["Scenario"] == "Original"][
        "Estimated Profit"
    ].sum()
    st.markdown("### 💰 Lucro Total por Cenário")
    col1, col2 = st.columns(2)
    col1.metric("Cenário Original", f"R$ {total_original:,.2f}")
    col2.metric("Cenário Simulado", f"R$ {total_simulado:,.2f}")


# ===========================
# APLICAÇÃO STREAMLIT
# ===========================


def main():
    st.set_page_config(page_title="Simulador de Precificação", layout="wide")
    st.title("🧠 Simulador de Estratégia de Preço (Análise What-If)")

    df_raw = load_and_clean_data("online_retail.csv")
    df_products = aggregate_data(df_raw)

    st.sidebar.header("Configurações da Estratégia")
    profit_margin = (
        st.sidebar.slider(
            "Margem de Lucro (%)",
            0,
            100,
            30,
            5,
            help="Define a margem de lucro aplicada sobre o custo estimado.",
        )
        / 100
    )
    elasticity = st.sidebar.slider(
        "Insatisfação do Cliente (Elasticidade)",
        0.0,
        1.0,
        0.0,
        0.01,
        help="Define o quanto a demanda reage a mudanças na margem.",
    )

    df_base = simulate_baseline(df_products)
    df_simulated = simulate_strategy(df_products, elasticity, profit_margin)
    df_combined = pd.concat([df_base, df_simulated])

    st.subheader("📊 Lucro Mensal Estimado por Cenário")
    plot_profit_by_month(df_combined, df_raw)


if __name__ == "__main__":
    main()
