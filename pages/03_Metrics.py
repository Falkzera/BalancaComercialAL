# Importação das bibliotecas
import streamlit as st
import pandas as pd

# Base de dados
file = 'SerieExportacoesAL.csv'
df = pd.read_csv(file)

# Adicionando em outras páginas
st.session_state['df'] = df

# Layout da Página
st.set_page_config(layout='wide', page_title='Metrics', page_icon='📊')

# Títulos
st.title('Análise geral das exportações - Alagoas')
st.caption('**Fonte**: Governo Federal')

# Seletores de filtro
anos_disponiveis = df['CO_ANO'].unique()
meses_disponiveis = sorted(df['CO_MES'].unique())  # Ordenando os meses em ordem crescente
municipios_disponiveis = list(df['Nome_Município'].unique())
municipios_disponiveis.append('Alagoas')  # Adicionando "Alagoas" como opção

municipio_selecionado = st.sidebar.selectbox('Selecione o município:', municipios_disponiveis)
ano_selecionado = st.sidebar.select_slider('Selecione o ano:', anos_disponiveis)
mes_selecionado = st.sidebar.select_slider('Selecione o mês:', meses_disponiveis)

# Filtrando o DataFrame
if municipio_selecionado == 'Alagoas':
    df_filtrado = df[(df['CO_ANO'] == ano_selecionado) & 
                     (df['CO_MES'] == mes_selecionado)]
else:
    df_filtrado = df[(df['CO_ANO'] == ano_selecionado) & 
                     (df['CO_MES'] == mes_selecionado) & 
                     (df['Nome_Município'] == municipio_selecionado)]

# Mostrar por escrito o que foi selecionado
st.write(f'**Município**: {municipio_selecionado}')
st.write(f'**Ano**: {ano_selecionado}')
st.write(f'**Mês**: {mes_selecionado}')

# Verificando se o DataFrame filtrado está vazio
if df_filtrado.empty:
    st.warning('Não possui dados para o período mencionado.')
else:
    # Métricas daframe
    # Parceiros comerciais com mais exportações
    st.header('Principais Parceiros Comerciais')
    st.bar_chart(df_filtrado.groupby('NO_PAIS')['VL_FOB'].sum().sort_values(ascending=False).head(10))

    # Produtos mais exportados
    st.header('Principais Produtos Exportados')
    st.bar_chart(df_filtrado.groupby('SH4')['VL_FOB'].sum().sort_values(ascending=False).head(10))

    # Municípios com mais exportações
    if municipio_selecionado == 'Alagoas':
        st.header('Municípios com mais exportações')
        st.bar_chart(df_filtrado.groupby('Nome_Município')['VL_FOB'].sum().sort_values(ascending=False).head(10))
    
# Cŕeditos
with st.sidebar:
    st.markdown('---')
    social_media_html = """
    <div style="text-align: center;">
        <h2>Redes Sociais</h2>
        <a href="https://www.instagram.com/falkzera/" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram" style="width:40px;height:40px;margin:10px;">
        </a>
        <a href="https://github.com/falkzera" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub" style="width:40px;height:40px;margin:10px;">
        </a>
        <p style="text-align: center;">Developer by: <a href="https://GitHub.com/Falkzera" target="_blank">Lucas Falcão</a></p>
    </div>
    """
    st.markdown(social_media_html, unsafe_allow_html=True)
    
