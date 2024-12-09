# Importação das bibliotecas
import streamlit as st
import pandas as pd

# Layout da Página
st.set_page_config(layout='wide', page_title='Introdução', page_icon='House')

# Títulos
st.title('Balança Comercial de Alagoas')
st.subheader('Uma série história: 1997 - 2024')
st.caption('**Fonte**: Governo Federal')

with st.sidebar:
    social_media_html = """
    <div style="text-align: center;">
        <h2>Redes Sociais</h2>
        <a href="https://www.instagram.com/falkzera/" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram" style="width:40px;height:40px;margin:10px;">
        </a>
        <a href="https://github.com/falkzera" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub" style="width:40px;height:40px;margin:10px;">
        </a>
        <a href="https://www.linkedin.com/in/falkzera/" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/e/e9/Linkedin_icon.svg" alt="LinkedIn" style="width:40px;height:40px;margin:10px;">
        </a>
        <p style="text-align: center;">Developer by: <a href="https://GitHub.com/Falkzera" target="_blank">Lucas Falcão</a></p>
    </div>
    """
    st.markdown(social_media_html, unsafe_allow_html=True)

st.markdown(
    """
    Bem-vindo ao **Dashboard de Exportações e Importações do Estado de Alagoas**.  
    Este projeto foi desenvolvido para permitir uma análise interativa e detalhada das atividades de comércio exterior do estado, com foco em:
    - Exportações e importações por município.
    - Produtos mais comercializados.
    - Principais parceiros comerciais.

    ---
    """
)

st.header("📋 Como Utilizar")
st.markdown(
    """
    Para explorar os dados disponíveis, siga os passos abaixo:

    1. **Filtrar o Período**  
       - Utilize os filtros disponíveis para selecionar o intervalo de tempo desejado (1997 a novembro de 2024).
       - Selecione meses e anos específicos para análises detalhadas.

    2. **Escolher o Município**  
       - Analise as exportações e importações de um município específico de Alagoas.
       - Compare o desempenho entre diferentes municípios.

    3. **Visualizar os Dados**  
       - Navegue pelas abas disponíveis para ver gráficos interativos, tabelas e mapas.
       - Explore os produtos mais exportados e importados, além dos parceiros comerciais.

    ---
    """
)

st.header("📚 Informações Adicionais")
st.markdown(
    """
    - Este dashboard foi desenvolvido utilizando **Streamlit** e **Python**.
    - Os dados são atualizados mensalmente, abrangendo as atividades comerciais de **1997 a 2024**.

    Caso tenha dúvidas ou sugestões, entre em contato pelas redes sociais.

    ---
    """
)



