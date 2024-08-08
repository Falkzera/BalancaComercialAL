# Importação das bibliotecas
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Base de dados
file = 'SerieExportacoesAL.csv'
df = pd.read_csv(file)

# Adicionando em outras páginas
st.session_state['df'] = df

# Layout da Página
st.set_page_config(layout='wide', page_title='Analysis', page_icon='📊')

# Títulos
st.title('Análise geral das exportações - Alagoas')
st.subheader('Uma série história: 1997 - 2024')
st.caption('**Fonte**: Governo Federal')

# FIltro Municípal
municipio = df['Nome_Município'].value_counts().index.tolist()
municipio.insert(0, 'Alagoas')

# SiderBar, Seleção do Município
controlador_municipio = st.sidebar.selectbox('Selecione o Município:', options=municipio)

# Definição do Option Menu

with st.container():
    selected = option_menu(
        menu_title = None,
        options = ['Série Anual', 'Série Mensal'],
        icons = ['file-text','calendar'],
        orientation='horizontal')

    # Série Anual
    if selected == 'Série Anual':

        # FIltro de Data
        ano_inicial = st.sidebar.selectbox('Selecione a data inicial:', df['CO_ANO'].unique())
        anos_disponiveis = df[df['CO_ANO'] > ano_inicial]['CO_ANO'].unique()
        ano_final = st.sidebar.selectbox('Selecione a data final:', anos_disponiveis, index=len(anos_disponiveis) - 1)

        # Condicional a partir das escolhas nos filtros da barra lateral
        if controlador_municipio == 'Alagoas':
            df_filtrado = df[(df['CO_ANO'] >= ano_inicial) & (df['CO_ANO'] <= ano_final)]
            df_filtrado = df_filtrado.groupby('CO_ANO').sum().reset_index()
        else:
            df_filtrado = df[(df['Nome_Município'] == controlador_municipio) & 
                            (df['CO_ANO'] >= ano_inicial) & 
                            (df['CO_ANO'] <= ano_final)]
        
        # Criação de uma instância que aponta para o DataFrame original.
        df_filtrado1 = df_filtrado
       
        # Mensagens na tela
        st.header(f'**{controlador_municipio}:**  Período de **{ano_inicial}** até **{ano_final}**')
        # Informações metrícas
        st.subheader(f"Valor total: US$ **{df_filtrado['VL_FOB'].sum():,.2f}**")
        # Gráfico de linha
        # Adicionar condicional de que se vazio, não aparecer nada
        if not df_filtrado.empty:
            # st.subheader(f'Exportações')
            st.line_chart(df_filtrado.groupby('CO_ANO')['VL_FOB'].sum())  
        # Se não houver dados, exibir mensagem
        else:    
            st.write('Não há gŕaficos disponíveis para a seleção realizada.')
       
        # Utilizado o valor apontado para a instância original
        # Se estiver vazio, não aparecer nada
        if not df_filtrado.empty:
            if controlador_municipio != 'Alagoas':
                # Parceiros Comérciais
                st.header("Parceiros comerciais")  
                st.subheader("Ranking dos 5 maiores parceiros comerciais")  
                
                resultado = df_filtrado1.groupby('NO_PAIS')['VL_FOB'].sum().sort_values(ascending=False).head(5)
                st.write(resultado)
        else:
            st.write('Não há parceiros comerciais disponíveis para a seleção realizada.')

            
    # Série Mensal
    elif selected == 'Série Mensal':

        ano_selecionado = st.sidebar.select_slider('Selecione o Ano:', df['CO_ANO'].unique())

        # Filtro de Intervalo de Meses
        mes_inicial = st.sidebar.selectbox('Selecione o mês inicial:', range(1, 13))
        mes_final = st.sidebar.selectbox('Selecione o mês final:', range(1, 13), index=11)

        # Aplicando o filtro no DataFrame
        if controlador_municipio == 'Alagoas':
            df_filtrado = df[(df['CO_ANO'] == ano_selecionado) & 
                            (df['CO_MES'] >= mes_inicial) & 
                            (df['CO_MES'] <= mes_final)]
            df_filtrado = df_filtrado.groupby(['CO_ANO', 'CO_MES']).sum().reset_index()
        else:
            df_filtrado = df[(df['Nome_Município'] == controlador_municipio) & 
                            (df['CO_ANO'] == ano_selecionado) & 
                            (df['CO_MES'] >= mes_inicial) & 
                            (df['CO_MES'] <= mes_final)]

        # Aparecer escrito na tela o valor total de exportações no periodo selecionado com o nome do municipio escolhido
                # Criação de uma instância que aponta para o DataFrame original.
        df_filtrado1 = df_filtrado
       
        # Mensagens na tela
        st.header(f'**{controlador_municipio}:**  Mês de **{mes_inicial}** até **{mes_final}** do Ano **{ano_selecionado}**')
        # Informações metrícas
        st.subheader(f"Valor total: US$ **{df_filtrado['VL_FOB'].sum():,.2f}**")
        # Gráfico de linha
        # Adicionar condicional de que se vazio, não aparecer nada
        if not df_filtrado.empty:

            if mes_inicial != mes_final:
                st.line_chart(df_filtrado.groupby('CO_MES')['VL_FOB'].sum())  
        # Se CO_MES inicial for igual ao CO_MES final, exibir uma mensagem sem grafico

              
        # Se não houver dados, exibir mensagem
        else:    
            st.write('Não há gŕaficos disponíveis para a seleção realizada.')
       
        # Utilizado o valor apontado para a instância original
        # Se estiver vazio, não aparecer nada
        if not df_filtrado.empty:
            if controlador_municipio != 'Alagoas':
                # Parceiros Comérciais
                st.header("Parceiros comerciais")  
                st.subheader("Ranking dos 5 maiores parceiros comerciais")  
                
                resultado = df_filtrado1.groupby('NO_PAIS')['VL_FOB'].sum().sort_values(ascending=False).head(5)
                st.write(resultado)
                
        else:
            st.write('Não há parceiros comerciais disponíveis para a seleção realizada.')


# Configurações da Barra Lateral e cŕeditos

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
    
