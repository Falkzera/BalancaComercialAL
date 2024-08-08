# Importação das bibliotecas
import streamlit as st
import pandas as pd

# Base de dados
file = 'SerieExportacoesAL.csv'
df = pd.read_csv(file)

# Layout da Página
st.set_page_config(layout='centered', page_title='Exportações em Alagoas - Análise de Dados :bar_chart:')

# Títulos
st.title('Exportações em Alagoas')
st.subheader('Uma série história: 1997 - 2024')
st.caption('**Fonte**: Governo Federal')

# Configurações da Barra Lateral
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
    

st.subheader("Sobre o Projeto 🎯")

st.markdown("""
    <div style="text-align: justify;">
        <p>Este projeto é um estudo de caso sobre as exportações do estado de Alagoas, baseado em dados fornecidos pelo Governo Federal. O objetivo principal é analisar o comportamento das exportações ao longo dos anos, identificando os seguintes aspectos:</p>
        <ul>
            <li>Principais parceiros comerciais</li>
            <li>Produtos exportados</li>
            <li>Municípios exportadores</li>
        </ul>
        <p>O projeto foi dividido em duas etapas:</p>
        <ol>
            <li><strong>Extração e Filtragem da Base de Dados:</strong> 
                <p>Na primeira etapa, foi realizada a extração da base de dados do Governo Federal, contendo informações sobre as exportações do Brasil. Inicialmente, a base possuía <strong>20.139.345</strong> linhas. Utilizando a linguagem de programação Python e a biblioteca Pandas, a base foi filtrada para incluir apenas os dados referentes ao estado de Alagoas.</p>
                <p>Como a base de dados original não incluía o nome dos municípios, foi necessário cruzar os dados com uma outra base para identificar a origem das exportações e os parceiros comerciais.</p>
            </li>
            <li><strong>Criação da Interface Gráfica:</strong>
                <p>Na segunda etapa, foi desenvolvida uma interface gráfica interativa com a biblioteca Streamlit. Esta interface permite ao usuário:</p>
                <ul>
                    <li>Selecionar o município, ano e mês desejados</li>
                    <li>Visualizar gráficos com as principais informações sobre exportações</li>
                </ul>
                <p>Com a interface gráfica, é possível observar os principais parceiros comerciais, produtos exportados e municípios exportadores, bem como outras informações relevantes. Esta funcionalidade é crucial para a identificação de soluções de negócios e para descobrir possíveis gargalos e oportunidades de melhoria.</p>
            </li>
        </ol>
        <p>O projeto foi desenvolvido por <strong>Lucas Falcão</strong>, estudante de Ciências Econômicas da Universidade Federal de Alagoas. Para mais informações, visite o <a href="https://github.com/Falkzera" target="_blank">perfil do desenvolvedor no GitHub</a>.</p>
    </div>
""", unsafe_allow_html=True)


