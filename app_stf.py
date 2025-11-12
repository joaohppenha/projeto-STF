import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


st.set_page_config(page_title="Dashboard STF", layout="wide")

# 1. Carregamento dados
@st.cache_data
def carregar_dados():
    df = pd.read_excel(r"C:\Users\joaoh\OneDrive\Área de Trabalho\Projeto_STF\decisoes_stf_limpo.xlsx")
    df = df[['nome_ministro', 'tempo_julgamento_dias', 'classe', 'ano da decisão',  'indicador_tramitacao', 'subgrupo andamento decisão', 'assuntos_processo']]
    df['tempo_julgamento_dias'] = pd.to_numeric(df['tempo_julgamento_dias'], errors='coerce')
    df.dropna(subset=['nome_ministro', 'tempo_julgamento_dias'], inplace=True)
    return df

df = carregar_dados()

st.title("Dashboard Interativo - Decisões do STF")

# 2. Filtros laterais
st.sidebar.header("Filtros")
ministros = st.sidebar.multiselect("Ministro:", df['nome_ministro'].unique(), default=df['nome_ministro'].unique())
classe = st.sidebar.multiselect("Classe:", df['classe'].dropna().unique(), default=df['classe'].dropna().unique())
tempo_min, tempo_max = st.sidebar.slider("Tempo de julgamento (dias):",
    int(df['tempo_julgamento_dias'].min()),
    int(df['tempo_julgamento_dias'].max()),
    (30, 500)
)

df_filtrado = df[
    (df['nome_ministro'].isin(ministros)) &
    (df['classe'].isin(classe)) &
    (df['tempo_julgamento_dias'].between(tempo_min, tempo_max))
]

st.markdown(f"**Total de registros filtrados:** {len(df_filtrado)}")




# 2.  Medidas: 

# total de ações  - contagem de linhas de ações
total_acoes = df["classe"].dropna().shape[0]
# Total de Ministros - contagem de nomes únicos

total_ministros = df["nome_ministro"].nunique()

#Total de Dias de julgamentos

total_tempo_julgamento = df["tempo_julgamento_dias"].sum()

# Contagem de  linhas com "DECISÃO FINAL" na coluna
total_decisoes_finais = (df["subgrupo andamento decisão"] == "DECISÃO FINAL").sum()

# Contagem de Ações em Tramitação
total_tramitacao = df["indicador_tramitacao"].dropna().str.strip().str.upper().eq("SIM").sum()


# 3. Cards

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    # Card com o total de ações
    st.metric("Total de Ações do STF", f"{total_acoes:,}")

with col2:
    # Card com o total de ministros
    st.metric("Total de Ministros", f"{total_ministros:,}")

with col3:
    # Card total de dias de julgamento
    st.metric("Total de Tempo de Julgamento (dias)", f"{total_tempo_julgamento:,}")

with col4:
    # Card de decisões finais
    st.metric("Decisões Finais", f"{total_decisoes_finais:,}")

with col5:
    # Card de ações em tramitação
    st.metric("Ações em Tramitação", f"{total_tramitacao:,}")



col6, col7 = st.columns(2)


# Gráficos


#Formatação

def format_plot(fig):
    fig.update_layout(
        title_x=0.5,
        autosize=True,
        margin=dict(t=80, b=40, l=40, r=40),
    )
    fig.update_xaxes(tickangle=-45, automargin=True)
    fig.update_yaxes(automargin=True)
    return fig



# === Agrupamento por CLASSE ===
decisoes_por_classe = (
    df[df["subgrupo andamento decisão"].str.upper().str.strip() == "DECISÃO FINAL"]
    .groupby("classe")
    .size()
    .reset_index(name="total_decisoes_finais")
)

# Gráficos de Barras
decisoes_por_ministro = (
    df[df["subgrupo andamento decisão"].str.upper().str.strip() == "DECISÃO FINAL"]
    .groupby("nome_ministro")
    .size()
    .reset_index(name="total_decisoes_finais")
)

col8, col9 = st.columns(2)

with col8:
    # Gráfico 1 - Decisões Finais por Classe (barras verticais)
    fig1 = px.bar(
        decisoes_por_classe,
        x="classe",
        y="total_decisoes_finais",
        color="classe",
        text="total_decisoes_finais",
        title="Decisões  por tipo de Ação",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig1.update_traces(textposition="outside")
    fig1.update_layout(
        xaxis_title="Classe",
        yaxis_title="Total de Decisões Finais",
        showlegend=False,
        title_x=0.5
    )
    st.plotly_chart(fig1, use_container_width=True)

with col9:
    # Gráfico 2 - Decisões Finais por Ministro (barras horizontais)
    fig2 = px.bar(
        decisoes_por_ministro,
        x="total_decisoes_finais",
        y="nome_ministro",
        orientation="h",
        color="nome_ministro",
        text="total_decisoes_finais",
        title="Decisões  por Ministro",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig2.update_traces(textposition="outside")
    fig2.update_layout(
        xaxis_title="Total de Decisões Finais",
        yaxis_title="Ministro",
        showlegend=False,
        title_x=0.5
    )
    st.plotly_chart(fig2, use_container_width=True)

# Gráfico de Linhas

with col6:
    # 3. Boxplot interativo
    st.subheader("Tempo de julgamento por ministro")
    fig1 = px.box(
        df_filtrado,
        x="nome_ministro",
        y="tempo_julgamento_dias",
        points="all",
        color="nome_ministro",
        title="Distribuição do tempo de julgamento"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col7:
    # 4. Gráfico de pizza
    st.subheader("Distribuição de ações por ministro")
    acoes_por_ministro = df_filtrado['nome_ministro'].value_counts().reset_index()
    acoes_por_ministro.columns = ['nome_ministro', 'qtd_acoes']

    fig2 = px.pie(
        acoes_por_ministro,
        values='qtd_acoes',
        names='nome_ministro',
        title="Participação dos ministros nas decisões"
    )
    st.plotly_chart(fig2, use_container_width=True)



# 5. Tabela com visualização condicional
st.subheader("Tabela de eficiência dos ministros")
tempo_medio = df_filtrado.groupby('nome_ministro')['tempo_julgamento_dias'].mean().reset_index()
eficiencia = pd.merge(acoes_por_ministro, tempo_medio, on='nome_ministro')
eficiencia['eficiencia'] = eficiencia['qtd_acoes'] / eficiencia['tempo_julgamento_dias']
eficiencia.sort_values(by='eficiencia', ascending=False, inplace=True)

st.dataframe(
    eficiencia.style.background_gradient(subset='eficiencia', cmap='Greens'),
    use_container_width=True
)


# 7. Exportar CSV
with st.expander("Exportar tabela de eficiência"):
    st.download_button(
        label="Baixar como CSV",
        data=eficiencia.to_csv(index=False),
        file_name="eficiencia_ministros.csv",
        mime="text/csv"
    )
