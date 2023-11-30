import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

df2 = pd.read_csv('vazao5_2.csv', sep=";")

#Alterando a pontuação do valor de vazão
df2['value'] = df2['value'].astype(str).str.replace(',', '.').astype(float)

# Selecionando somente a quality=good e removendo a coluna quality, pois temos todos os valores iguais
df2['quality'] = df2['quality'].str.strip().str.lower()
# df2 = df2[df2['quality'] == 'good']
df2 = df2.rename(columns={'value': 'vazao'})
#df2 = df2.drop(columns='quality')

#Alterando a coluna timestamp para timestramp e extraindo o dia da semana
df2['timestamp'] = pd.to_datetime(df2['timestamp'], dayfirst=True)
df2['day_of_week'] = df2['timestamp'].dt.dayofweek

# Mapeia o número do dia da semana para o nome do dia da semana em português
dias_da_semana = {2:'Segunda-feira', 3:'Terça-feira', 4:'Quarta-feira', 5:'Quinta-feira', 6:'Sexta-feira', 0:'Sábado', 1:'Domingo'}
df2['day_of_week_name'] = df2['day_of_week'].map(dias_da_semana)

##GRAFICO 1
df_vazao1 = df2.copy()
# Converte a coluna 'timestamp' para o tipo datetime
df_vazao1['timestamp'] = pd.to_datetime(df_vazao1['timestamp'])

# Extrai o dia da semana da coluna 'timestamp' e criar uma nova coluna 'day_of_week'
df_vazao1['day_of_week'] = df_vazao1['timestamp'].dt.dayofweek  # Segunda-feira: 0, Terça-feira: 1, ...

# Cria o gráfico de calendar heatmap
fig = px.density_heatmap(df_vazao1, x="day_of_week_name", y="timestamp", z="vazao", color_continuous_scale="Viridis", title="Variação da Vazão ao Longo da Semana")

# Personaliza o layout
fig.update_xaxes(title="Dia da Semana")
fig.update_yaxes(title="Mes e Ano")
fig.update_coloraxes(colorbar_title="Vazão (m³/s)")

## GRAFICO 2

# Dados climatológicos
df_clima = {
    "Mês": ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
    "Temperatura Média (°C)": [26.7, 27, 25.9, 24.3, 21.8, 20.8, 20.1, 20.9, 22.2, 23.7, 24.2, 25.8],
    "Temperatura Mínima (°C)": [23.3, 23.3, 22.7, 21.1, 18.2, 16.8, 16, 16.5, 18.1, 20, 21, 22.4],
    "Temperatura Máxima (°C)": [31.2, 31.7, 30.2, 28.5, 26.2, 25.8, 25.4, 26.5, 27.5, 28.6, 28.5, 30.1],
    "Chuva (mm)": [172, 117, 153, 99, 81, 52, 55, 45, 81, 98, 143, 156],
    "Umidade(%)": [79, 78, 81, 81, 81, 80, 79, 76, 75, 76, 80, 80],
    "Dias Chuvosos (d)": [12, 10, 12, 10, 9, 6, 6, 6, 8, 9, 12, 12],
    "Horas de Sol (h)": [9.8, 10.0, 8.8, 7.9, 7.2, 7.0, 6.9, 7.3, 7.2, 7.4, 7.7, 8.8]
}

mapa_meses = {
    'January': 'Janeiro',
    'February': 'Fevereiro',
    'March': 'Março',
    'April': 'Abril',
    'May': 'Maio',
    'June': 'Junho',
    'July': 'Julho',
    'August': 'Agosto',
    'September': 'Setembro',
    'October': 'Outubro',
    'November': 'Novembro',
    'December': 'Dezembro'
}

# Cria um DataFrame com os dados climatológicos
df_temperatura = pd.DataFrame(df_clima)

df_vazao2 = df2.copy()
df_vazao2['timestamp'] = pd.to_datetime(df_vazao2['timestamp'])

# Extraindo o mês da coluna 'timestamp' e criando uma nova coluna 'Mês'
df_vazao2['Mês'] = df_vazao2['timestamp'].dt.strftime('%B').map(mapa_meses)

# Mesclando os dois conjuntos de dados com base na coluna 'Mês'
merged_df = pd.merge(df_vazao2, df_temperatura, left_on='Mês', right_on='Mês', how='inner')
# merged_df

fig2 = px.scatter(merged_df, x='Temperatura Média (°C)', y='vazao', title='Relação entre Temperatura e Vazão',
                 labels={'vazao': 'Vazão', 'Temperatura Média (°C)': 'Temperatura Média (°C)'})


##GRAFICO 3

df = df2.copy()

df['timestamp'] = pd.to_datetime(df['timestamp'])

# Separa a informação de qualidade
df[['quality_status', 'quality_value']] = df['quality'].str.split(': ', expand=True)

# Mapea 'good' e 'bad' para valores booleanos
df['is_good'] = df['quality_status'] == 'good'
df['is_bad'] = df['quality_status'] == 'bad'

# Preenche valores NaN de 'vazao' com 0 para leituras ruins
df['vazao'].fillna(0, inplace=True)

# Adiciona coluna de dia da semana
df['day_of_week'] = df['timestamp'].dt.dayofweek
df['day_of_week_name'] = df['timestamp'].dt.day_name()

# Mapea os nomes dos dias da semana para português
dias_semana = {
    'Monday': 'Segunda-feira',
    'Tuesday': 'Terça-feira',
    'Wednesday': 'Quarta-feira',
    'Thursday': 'Quinta-feira',
    'Friday': 'Sexta-feira',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

df['day_of_week_name_pt'] = df['day_of_week_name'].map(dias_semana)

# Cria DataFrame separado para leituras ruins
bad_data = df[df['is_bad']]

# Classifica ambos os DataFrames pelos timestamps
df.sort_values(by='timestamp', inplace=True)
bad_data.sort_values(by='timestamp', inplace=True)

# Cria o gráfico
fig3 = px.scatter(df, x='timestamp', y='vazao', color='is_good', facet_col='day_of_week_name_pt', facet_col_wrap=3,
                 labels={'vazao': 'Vazão', 'is_good': 'Leitura Boa', 'timestamp': 'Timestamp'},
                 title='Variação na Qualidade das Leituras ao Longo da Semana')

# Adiciona trace para leituras ruins
if not bad_data.empty:
    fig3.add_trace(px.scatter(bad_data, x='timestamp', y='vazao', color='is_bad', facet_col='day_of_week_name_pt').data[0])

# Atualiza o layout
fig3.update_layout(showlegend=False)


# Inicializa o aplicativo Dash
app = dash.Dash(__name__)

# Layout do Dashboard
app.layout = html.Div(children=[
    # Gráfico 1: Variação da Vazão ao Longo da Semana
    dcc.Graph(
        id='graph1',
        figure=fig
    ),

    # Gráfico 2: Relação entre Temperatura e Vazão
    dcc.Graph(
        id='graph2',
        figure=fig2
    ),

    # Gráfico 3: Variação na Qualidade das Leituras ao Longo da Semana
    dcc.Graph(
        id='graph3',
        figure=fig3
    )

])

# Executa o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)