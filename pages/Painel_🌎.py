# Importação das bibliotecas
import streamlit as st
import pandas as pd
import json
import unidecode
import plotly.graph_objects as go
import plotly.express as px
from streamlit_option_menu import option_menu


st.set_page_config(layout='wide', page_title='Painel Balança Comercial Alagoas', page_icon='🌎')

# Títulos
st.title('Análise geral das exportações - Alagoas')
st.subheader('Uma série história: 1997 - 2024')
st.caption('**Fonte**: Governo Federal')

with st.container():  # CARREGAMENTO DATASET
    @st.cache_data
    def load_data():

        parquet_file = ('data/BALANCA-COMERCIAL.parquet')
        return pd.read_parquet(parquet_file)
    df = load_data()
    df = df.sort_values(by='DATA')

with st.container():  # CRIAÇÃO DE COLUNA MES E ANO
    df['CO_ANO'] = df['DATA'].dt.year
    df['CO_MES'] = df['DATA'].dt.month

with st.container():  # FUNÇÃO DE FORMATAÇÃO DE MOEDA
    def formatar_moeda(valor):
        formato_ingles = f"{valor:,.2f}"
        parte_inteira, parte_decimal = formato_ingles.split('.')
        parte_inteira = parte_inteira.replace(',', '.')
        formato_final = f"{parte_inteira},{parte_decimal}"

        return formato_final

with st.container():  # FILTRO DE MUNICÍPIO & SUA SIDEBAR

    municipio = df['NO_MUN'].value_counts().index.tolist()
    municipio.insert(0, 'Alagoas')

    # SiderBar, Seleção do Município
    controlador_municipio = st.selectbox('Selecione o Município:', options=municipio)

# Definição do Option Menu

with st.container(): # MENU
    selected = option_menu(
        menu_title = None,
        options = ['EXPORTAÇÃO', 'IMPORTAÇÃO'],
        icons = ['file-text','calendar'],
        orientation='horizontal')

    with st.container():  # EXPORTAÇÃO
        if selected == 'EXPORTAÇÃO':

            with st.container(): # CRIAÇÃO DATAFRAMDE EXPORTAÇÃO
                df_exportacao = df[df['CATEGORIA'] == 'EXPORTACAO'].reset_index(drop=True).copy()
                
            with st.container(): # FILTRO DE DATA (PERÍODO)
                ano_inicial, ano_final = st.slider(
                    'Selecione o intervalo de anos:',
                    min_value=df_exportacao['DATA'].dt.date.min(),
                    max_value=df_exportacao['DATA'].dt.date.max(),
                    value=(df_exportacao['DATA'].dt.date.min(), df_exportacao['DATA'].dt.date.max()),
                    format="YYYY-MM-DD"
                )
                df_exportacao_mapa = df_exportacao.copy()

            with st.container(): # FILTRO DE MUNICÍPIO / AGRUPADO ALAGOAS
                if controlador_municipio == 'Alagoas':
                    df_exportacao = df_exportacao[(df_exportacao['DATA'].dt.date >= ano_inicial) & (df_exportacao['DATA'].dt.date <= ano_final)]
                    df_exportacao = df_exportacao.groupby(['DATA', 'CO_ANO', 'CO_MES']).sum().reset_index()
                else:
                    df_exportacao = df_exportacao[(df_exportacao['NO_MUN'] == controlador_municipio) & 
                            (df_exportacao['DATA'].dt.date >= ano_inicial) & 
                            (df_exportacao['DATA'].dt.date <= ano_final)]
                    
            with st.container(): #TÍTULO & VOLUME DE EXPORTAÇÃO
                st.header(f'**:blue[{controlador_municipio.title()}]:**  Período de **{ano_inicial}** até **{ano_final}**')
                st.subheader(f"Valor total de Exportação (US$): {formatar_moeda(df_exportacao['VL_FOB'].sum())}")

            with st.container(): # GRÁFICO DE LINHA

                if not df_exportacao.empty:
                    if (ano_final.year - ano_inicial.year) < 2:
                        fig = go.Figure()

                        fig.add_trace(go.Bar(x=df_exportacao.groupby('DATA')['VL_FOB'].sum().index, 
                                            y=df_exportacao.groupby('DATA')['VL_FOB'].sum(), 
                                            name='Exportação'))

                        fig.update_layout(title='Exportação Mensal',template='plotly_dark')
                        st.plotly_chart(fig)

                    else:
                        fig = go.Figure()

                        fig.add_trace(go.Scatter(x=df_exportacao.groupby('DATA')['VL_FOB'].sum().index, 
                                                y=df_exportacao.groupby('DATA')['VL_FOB'].sum(), 
                                                mode='lines', 
                                                name='Exportação'))

                        fig.update_layout(title='Exportação Anual',template='plotly_dark')
                        st.plotly_chart(fig)
                else:    
                    st.write('Não há gŕaficos disponíveis para a seleção realizada.')

            with st.container(): # PARCEIROS COMERCIAIS e GRAIFCO DE ROSCA

                if not df_exportacao.empty:
                    if controlador_municipio != 'Alagoas':
                        st.header("Parceiros comerciais")  
                        st.subheader(f"Ranking dos maiores parceiros comerciais de :blue[{controlador_municipio.title()}]")  
                        resultado_paises = df_exportacao.groupby('NO_PAIS')['VL_FOB'].sum().sort_values(ascending=False).head(10)
                        resultado_paises_tabela = df_exportacao.groupby('NO_PAIS')['VL_FOB'].sum().sort_values(ascending=False).head(10)

                        resultado_paises_tabela = resultado_paises.apply(formatar_moeda)

                        col1, col2 = st.columns(2)
                        col1.table(resultado_paises_tabela.head(10))
                        
                        fig = go.Figure(data=[go.Pie(labels=resultado_paises.head(10).index, values=resultado_paises.head(10))])
                        fig.update_layout(title='Participação dos maiores parceiros comerciais',template='plotly_dark')
                        col2.plotly_chart(fig)

                        with st.expander('Detalhes dos produtos exportados'):
                            tabs = st.tabs([pais for pais in resultado_paises.index])

                            for i, pais in enumerate(resultado_paises.index):
                                with tabs[i]:
                                    st.subheader(f'Produtos exportados para :orange[{pais}]')
                                    produtos = df_exportacao[df_exportacao['NO_PAIS'] == pais].groupby('NO_SH4_POR')['VL_FOB'].sum().sort_values(ascending=False).head(5)
                                    total_valor = produtos.sum()
                                    produtos = produtos.reset_index()
                                    produtos['%'] = (produtos['VL_FOB'] / total_valor) * 100
                                    produtos['%'] = produtos['%'].map(lambda x: f'{x:.2f}%')
                                    produtos['VL_FOB'] = produtos['VL_FOB'].apply(formatar_moeda)
                                    st.table(produtos)

            with st.container():  # MAPA IMPORTAÇÃO
                            
                if controlador_municipio == 'Alagoas':

                    geojson_path = 'mapa/Alagoas_Mapa.geojson'
                    with open(geojson_path) as f:
                        geojson = json.load(f)

                    municipios_geojson = [feature['properties']['NM_MUN'] for feature in geojson['features']]

                    municipios = [municipio.title() for municipio in municipios_geojson]
                    for feature in geojson['features']:
                        nome_original = feature['properties']['NM_MUN']
                        nome_normalizado = unidecode.unidecode(nome_original).upper()
                        feature['properties']['NM_MUN'] = nome_normalizado
                        
                    df_exportacao_mapa = df_exportacao_mapa[
                        (df_exportacao_mapa['DATA'].dt.date >= ano_inicial) &
                        (df_exportacao_mapa['DATA'].dt.date <= ano_final)
                    ]

                    df_exportacao_mapa = df_exportacao_mapa.groupby(['NO_MUN']).agg({'VL_FOB': 'sum'}).reset_index()

                    fig = px.choropleth_mapbox(
                        df_exportacao_mapa,
                        geojson=geojson,
                        locations='NO_MUN',         
                        color='VL_FOB',             
                        featureidkey='properties.NM_MUN',  
                        color_continuous_scale="Viridis", 
                        range_color=(0, df_exportacao_mapa['VL_FOB'].max()),  
                        mapbox_style="carto-positron",  
                        zoom=8,                       
                        center={"lat": -9.6, "lon": -36.7},  
                        opacity=0.5,                  
                        labels={'VL_FOB': 'Valor FOB'},
                        title=f'Importação por Município do período de {ano_inicial} até {ano_final}',  # Título dinâmico
                        width=1920,
                        height=1080
                    )

                    st.plotly_chart(fig)

        elif selected == 'IMPORTAÇÃO':

            with st.container(): # CRIAÇÃO DATAFRAMDE IMPORTAÇÃO
                df_importacao = df[df['CATEGORIA'] == 'IMPORTACAO'].reset_index(drop=True).copy()
                
            with st.container(): # FILTRO DE DATA (PERÍODO)
                ano_inicial, ano_final = st.slider(
                    'Selecione o intervalo de anos:',
                    min_value=df_importacao['DATA'].dt.date.min(),
                    max_value=df_importacao['DATA'].dt.date.max(),
                    value=(df_importacao['DATA'].dt.date.min(), df_importacao['DATA'].dt.date.max()),
                    format="YYYY-MM-DD"
                )
                df_importacao_mapa = df_importacao.copy()

            with st.container(): # FILTRO DE MUNICÍPIO / AGRUPADO ALAGO
            
                if controlador_municipio == 'Alagoas':
                    df_importacao = df_importacao[(df_importacao['DATA'].dt.date >= ano_inicial) & (df_importacao['DATA'].dt.date <= ano_final)]
                    df_importacao = df_importacao.groupby(['DATA', 'CO_ANO', 'CO_MES']).sum().reset_index()
                else:
                    df_importacao = df_importacao[(df_importacao['NO_MUN'] == controlador_municipio) & 
                            (df_importacao['DATA'].dt.date >= ano_inicial) & 
                            (df_importacao['DATA'].dt.date <= ano_final)]
                
            with st.container(): #TÍTULO & VOLUME DE IMPORTAÇÃO
            
                st.header(f'**:blue[{controlador_municipio.title()}]:**  Período de **{ano_inicial}** até **{ano_final}**')
                st.subheader(f"Valor total de Importação (US$): {formatar_moeda(df_importacao['VL_FOB'].sum())}")

            with st.container(): # GRÁFICO DE LINHA
            
                if not df_importacao.empty:
                    if (ano_final.year - ano_inicial.year) < 2:
                        fig = go.Figure()

                        fig.add_trace(go.Bar(x=df_importacao.groupby('DATA')['VL_FOB'].sum().index, 
                                            y=df_importacao.groupby('DATA')['VL_FOB'].sum(), 
                                            name='Importação'))

                        fig.update_layout(title='Importação Mensal',template='plotly_dark')
                        st.plotly_chart(fig)

                    else:
                        fig = go.Figure()

                        fig.add_trace(go.Scatter(x=df_importacao.groupby('DATA')['VL_FOB'].sum().index, 
                                                y=df_importacao.groupby('DATA')['VL_FOB'].sum(), 
                                                mode='lines', 
                                                name='Importação'))

                        fig.update_layout(title='Importação Anual',template='plotly_dark')
                        st.plotly_chart(fig)
                else:    
                    st.write('Não há gŕaficos disponíveis para a seleção realizada.')

            if not df_importacao.empty:
                if controlador_municipio != 'Alagoas':
                    st.header("Parceiros comerciais")  
                    st.subheader(f"Ranking dos maiores parceiros comerciais de :blue[{controlador_municipio.title()}]")  
                    resultado_paises = df_importacao.groupby('NO_PAIS')['VL_FOB'].sum().sort_values(ascending=False).head(10)
                    resultado_paises_tabela = df_importacao.groupby('NO_PAIS')['VL_FOB'].sum().sort_values(ascending=False).head(10)
                    resultado_paises_tabela = resultado_paises.apply(formatar_moeda)

                    col1, col2 = st.columns(2)
                    col1.table(resultado_paises_tabela.head(10))
                    
                    fig = go.Figure(data=[go.Pie(labels=resultado_paises.head(10).index, values=resultado_paises.head(10))])
                    fig.update_layout(title='Participação dos maiores parceiros comerciais',template='plotly_dark')
                    col2.plotly_chart(fig)

                    st.info('Clique no botão para ver os detalhes dos produtos importados')
                    with st.expander('Detalhes dos produtos importados'):
                        tabs = st.tabs([pais for pais in resultado_paises.index])

                        for i, pais in enumerate(resultado_paises.index):
                            with tabs[i]:
                                st.subheader(f'Produtos importados de :orange[{pais}]')
                                produtos = df_importacao[df_importacao['NO_PAIS'] == pais].groupby('NO_SH4_POR')['VL_FOB'].sum().sort_values(ascending=False).head(5)
                                total_valor = produtos.sum()
                                produtos = produtos.reset_index()
                                produtos['%'] = (produtos['VL_FOB'] / total_valor) * 100
                                produtos['%'] = produtos['%'].map(lambda x: f'{x:.2f}%')
                                produtos['VL_FOB'] = produtos['VL_FOB'].apply(formatar_moeda)
                                st.table(produtos)

            with st.container():  # MAPA IMPORTAÇÃO
                            
                if controlador_municipio == 'Alagoas':

                    geojson_path = 'mapa/Alagoas_Mapa.geojson'
                    with open(geojson_path) as f:
                        geojson = json.load(f)

                    municipios_geojson = [feature['properties']['NM_MUN'] for feature in geojson['features']]

                    municipios = [municipio.title() for municipio in municipios_geojson]
                    for feature in geojson['features']:
                        nome_original = feature['properties']['NM_MUN']
                        nome_normalizado = unidecode.unidecode(nome_original).upper()
                        feature['properties']['NM_MUN'] = nome_normalizado

                    df_importacao_mapa = df_importacao_mapa[
                        (df_importacao_mapa['DATA'].dt.date >= ano_inicial) &
                        (df_importacao_mapa['DATA'].dt.date <= ano_final)
                    ]

                    df_importacao_mapa = df_importacao_mapa.groupby(['NO_MUN']).agg({'VL_FOB': 'sum'}).reset_index()

                    fig = px.choropleth_mapbox(
                        df_importacao_mapa,
                        geojson=geojson,
                        locations='NO_MUN',          
                        color='VL_FOB',              
                        featureidkey='properties.NM_MUN', 
                        color_continuous_scale="Viridis",  
                        range_color=(0, df_importacao_mapa['VL_FOB'].max()),  
                        mapbox_style="carto-positron",  
                        zoom=8,                        
                        center={"lat": -9.6, "lon": -36.7},  
                        opacity=0.5,                    
                        labels={'VL_FOB': 'Valor FOB'}, 
                        title=f'Importação por Município do período de {ano_inicial} até {ano_final}',
                        width=1920,
                        height=1080
                    )

                    st.plotly_chart(fig)

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
