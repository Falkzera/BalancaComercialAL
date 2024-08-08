import pandas as pd
import plotly.express as px
import streamlit as st
import json

# Layout da Página
st.set_page_config(layout='wide', page_title='Map', page_icon='🗺️')

# Função para formatar números com abreviação
def format_value(value):
    if value >= 1_000_000_000:
        return f'{value / 1_000_000_000:.1f}B'
    elif value >= 1_000_000:
        return f'{value / 1_000_000:.1f}M'
    else:
        return f'{value:.1f}'

# Base de dados
file = 'SerieExportacoesAL.csv'
df = pd.read_csv(file)

# Adicionando em outras páginas
st.session_state['df'] = df


#  Títulos
st.title('Análise geral das exportações - Alagoas')
st.caption('**Fonte**: Governo Federal')

# Carregar o arquivo GeoJSON dos municípios de Alagoas
geojson_path = 'mapa/Alagoas_Mapa.geojson'  # Substitua pelo caminho do seu arquivo GeoJSON
with open(geojson_path) as f:
    geojson = json.load(f)

# Extrair os nomes dos municípios do GeoJSON
municipios_geojson = [feature['properties']['NM_MUN'] for feature in geojson['features']]

# Definir uma lista de temas
temas = ['Blues', 'Cividis', 'Plasma', 'Inferno', 'Magma']

# Criar um menu suspenso com alguns temas
tema_selecionado = st.sidebar.selectbox('Selecione o tema do mapa:', temas)

# Filtro de Data
ano_inicial = df['CO_ANO'].min()  # Fixar a data inicial no último ano disponível
anos_disponiveis = df['CO_ANO'].unique()
ano_final = st.sidebar.slider('Selecione a data final:', min_value=ano_inicial, max_value=anos_disponiveis.max(), value=ano_inicial)

# Filtrar os dados com base nos filtros de data
df_filtrado = df[(df['CO_ANO'] >= ano_inicial) & (df['CO_ANO'] <= ano_final)]

# Agrupar os dados por município e somar os valores
df_filtrado = df_filtrado.groupby('Nome_Município').sum().reset_index()

# Garantir que todos os municípios estejam presentes no DataFrame
df_completo = pd.DataFrame(municipios_geojson, columns=['Nome_Município'])
df_completo = df_completo.merge(df_filtrado, on='Nome_Município', how='left').fillna(0)

# Definir o valor mínimo fixo em 0
valor_minimo = 0

# Slider para o valor máximo com legenda "Valor em US$"
valor_maximo = st.sidebar.slider(
    'Valor em US$:',
    min_value=float(df_completo['VL_FOB'].min()),  # Valor mínimo do slider é o valor mínimo dos dados
    max_value=float(df_completo['VL_FOB'].max()) + 1_000_000,  # Valor máximo do slider é 1 milhão acima do máximo dos dados
    value=float(df_completo['VL_FOB'].mean()) + 1_000_000,  # Valor inicial do slider
    format="$%.0f"  # Formato dos valores do slider
)

# Exibir o valor formatado
st.sidebar.write(f'Valor Selecionado: {format_value(valor_maximo)}')


# Mostrar para o usuario o periodo que ele escolheu
st.subheader(f'**Período Selecionado**: {ano_inicial} - {ano_final}')
st.write(f'**Valor Filtrado**: {format_value(valor_maximo)}')

# Função para criar o mapa coroplético
def make_choropleth(input_df, geojson, input_id, input_column, input_color_theme, valor_minimo, valor_maximo):
    choropleth = px.choropleth(
        input_df,
        geojson=geojson,
        locations=input_id,
        featureidkey="properties.NM_MUN",  # Ajuste aqui para corresponder à chave correta no seu GeoJSON
        color=input_column,
        color_continuous_scale=input_color_theme,
        range_color=(valor_minimo, valor_maximo),
        scope="south america",
        labels={input_column: 'Valor'}
    )
    choropleth.update_geos(fitbounds="locations", visible=False)
    choropleth.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=900
    )
    return choropleth

# Parâmetros para a função
input_id = 'Nome_Município'  # Nome da coluna no DataFrame com os nomes dos municípios
input_column = 'VL_FOB'     # Nome da coluna no DataFrame com os valores

# Gerar o choropleth com os dados completos e o tema selecionado
choropleth_fig = make_choropleth(df_completo, geojson, input_id, input_column, tema_selecionado, valor_minimo, valor_maximo)

# Exibir o choropleth usando Streamlit
st.plotly_chart(choropleth_fig)


# Créditos
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
    
