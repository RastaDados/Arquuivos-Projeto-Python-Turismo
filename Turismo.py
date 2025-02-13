import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
def load_data():
    file_path = "world_tourism_economy_data.csv"
    df = pd.read_csv(file_path)
    return df

df = load_data()

# Tratamento dos dados
df.dropna(subset=['tourism_receipts', 'tourism_arrivals', 'gdp'], inplace=True)
df['tourism_contribution_gdp'] = (df['tourism_receipts'] / df['gdp']) * 100

# Criando o Dashboard no Streamlit
st.set_page_config(page_title="Dashboard de Turismo", layout="wide")
st.sidebar.title("Navegação")
page = st.sidebar.radio("Selecione a Página", ["Turismo Global", "Turismo e Economia", "Gastos e Movimentação", "Tendências e Crescimento"])

if page == "Turismo Global":
    st.title("Turismo Global")
    
    # Gráfico 1: Chegadas de turistas ao longo dos anos
    arrivals_by_year = df.groupby("year")['tourism_arrivals'].sum().reset_index()
    fig1 = px.line(arrivals_by_year, x='year', y='tourism_arrivals', title="Evolução das Chegadas de Turistas")
    st.plotly_chart(fig1)
    
    # Gráfico 2: Top 10 países com mais turistas
    top_countries = df.groupby("country")['tourism_arrivals'].sum().nlargest(10).reset_index()
    fig2 = px.bar(top_countries, x='country', y='tourism_arrivals', title="Top 10 Países com Mais Turistas")
    st.plotly_chart(fig2)
    
    # Gráfico 3: Receitas de turismo por país
    top_revenue = df.groupby("country")['tourism_receipts'].sum().nlargest(10).reset_index()
    fig3 = px.bar(top_revenue, x='country', y='tourism_receipts', title="Top 10 Países com Maior Receita de Turismo")
    st.plotly_chart(fig3)

elif page == "Turismo e Economia":
    st.title("Turismo e Economia")
    
    # Gráfico 1: Contribuição do turismo no PIB
    fig4 = px.scatter(df, x='gdp', y='tourism_receipts', color='country', title="Receita de Turismo vs PIB")
    st.plotly_chart(fig4)
    
    # Gráfico 2: Turismo vs Inflação
    fig5 = px.scatter(df, x='inflation', y='tourism_receipts', color='country', title="Impacto da Inflação no Turismo")
    st.plotly_chart(fig5)
    
    # Gráfico 3: Turismo vs Desemprego
    fig6 = px.scatter(df, x='unemployment', y='tourism_receipts', color='country', title="Correlação entre Turismo e Desemprego")
    st.plotly_chart(fig6)

elif page == "Gastos e Movimentação":
    st.title("Gastos e Movimentação de Turistas")
    
    # Gráfico 1: Exportações e Gastos com Turismo
    fig7 = px.scatter(df, x='tourism_exports', y='tourism_expenditures', color='country', title="Exportações vs Gastos com Turismo")
    st.plotly_chart(fig7)
    
    # Gráfico 2: Países que mais emitem turistas
    top_departures = df.groupby("country")['tourism_departures'].sum().nlargest(10).reset_index()
    fig8 = px.bar(top_departures, x='country', y='tourism_departures', title="Top 10 Países que Mais Emitem Turistas")
    st.plotly_chart(fig8)
    
    # Gráfico 3: Relação entre Turismo Receptivo e Emissivo
    fig9 = px.scatter(df, x='tourism_arrivals', y='tourism_departures', color='country', title="Relação entre Turismo Receptivo e Emissivo")
    st.plotly_chart(fig9)

elif page == "Tendências e Crescimento":
    st.title("Tendências e Crescimento do Turismo")
    
    # Gráfico 1: Crescimento do turismo ao longo dos anos
    growth = df.groupby("year")['tourism_arrivals'].sum().pct_change().reset_index()
    fig10 = px.line(growth, x='year', y='tourism_arrivals', title="Crescimento Percentual do Turismo ao Longo dos Anos")
    st.plotly_chart(fig10)
    
    # Gráfico 2: Previsão de crescimento do turismo (média móvel)
    df['rolling_mean'] = df.groupby('country')['tourism_arrivals'].transform(lambda x: x.rolling(3, min_periods=1).mean())
    fig11 = px.line(df, x='year', y='rolling_mean', color='country', title="Média Móvel do Turismo por País")
    st.plotly_chart(fig11)
    
    # Gráfico 3: Comparação entre crescimento econômico e turismo
    df['gdp_growth'] = df.groupby('country')['gdp'].pct_change()
    fig12 = px.scatter(df, x='gdp_growth', y='tourism_arrivals', color='country', title="Crescimento do PIB vs Turismo")
    st.plotly_chart(fig12)
