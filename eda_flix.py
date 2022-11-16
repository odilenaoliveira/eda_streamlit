import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
from collections import Counter
from dataset import features, loadData, text_freq
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

#todo: carregando os dados
df = loadData()
durations = features(df)

#* agrupamento dos dados
country = df['country'].value_counts().reset_index().head(10)
rating = df['rating'].value_counts().reset_index()

tipo = df[['type','year_added',
'month_added','day_added']].groupby(['type','year_added',
'month_added','day_added']).count().reset_index()

#todo: estilização da página
st.title('Tipo de entreterimento: NETFLIX')

st.write('### Tabelas')
#? ------- tabelas --------
with st.expander('Os Dez países que mais produzem filmes'):
    st.write(country)
    fig = plt.figure(figsize=(14,8))
    sns.countplot(y=df['country'], order=df['country'].value_counts().index[0:10], palette='Set2')
    plt.yticks(fontsize=16)
    plt.tight_layout()
    st.pyplot(fig)

with st.expander('Ano de lançamento dos conteúdos'):
    fig0 = plt.figure(figsize=(8,16))
    sns.countplot(y=df['release_year'], order=df['release_year'].value_counts().index, palette='Set2')
    plt.title('Ano de Lançamento dos conteúdos', fontsize=16)
    plt.tight_layout()
    st.pyplot(fig0)

with st.expander('Qual o filme mais antigo'):
    antigo = df.sort_values('release_year', ascending=True)
    antigo = antigo[antigo['duration'] != ""]
    antigo[['title', 'release_year']][:15]

with st.expander('Qual foi o filme mais recente'):
    recente = df.sort_values('release_year', ascending=False)
    recente = recente[recente['duration'] != ""]
    recente[['title', 'release_year']][:15]

with st.expander('Quais o tipo de avaliações'):
    st.write(rating)
    fig = plt.figure(figsize=(14,7))
    sns.countplot(x=df['rating'], order=df['rating'].value_counts().index[0:10], palette='Set2')
    st.pyplot(fig)

with st.expander('Qual serie teve mais temporadas'):
    seasons = durations.loc[(durations['number_of_seasons'] >= 1) & (durations['number_of_seasons'] <= 17)]
    t = ['title', 'number_of_seasons']
    top = seasons[t]
    top = top.sort_values(by='number_of_seasons', ascending=False)
    st.write(top.head(20))

with st.expander('Categorias mais adicionadas'):
    cat = df['listed_in'].value_counts().head(20)
    st.write(cat)

#? -------- carrossel --------
st.write('### Tipo de entreterimento adicionado ao longo dos anos')
st.text('''
Selecione o ano e veja nos gráficos abaixo, os meses, os dias, e o tipo de conteúdo
adicionados ao longo dos anos
''')
# filtro mesclado com o agrupamento
ano = st.selectbox('Escolha o ano:', tipo['year_added'].unique())
year = tipo[tipo['year_added'] == ano]

#? ---------- tabelas carrossel -----------
tab1, tab2, tab3,tab4,tab5 = st.tabs(['gráfico1','gráfico2','gráfico3','gráfico4','gráfico5'])

with tab1:
    color = ['#00CED1', '#3CB371']
    fig1 = plt.figure(figsize=(14,7))
    sns.countplot(x=year['type'], palette=color)
    plt.title('Tipo de entreterimento', fontsize=16)
    plt.xticks(fontsize=16)
    st.pyplot(fig1)

with tab2:
    fig2 = plt.figure(figsize=(14,7))
    valor = year['type'].value_counts()
    labels = ['Movie','TV Show']
    explode = (0,0.1)
    color = ['#00CED1', '#3CB371']
    plt.pie(valor, labels=labels, explode=explode, autopct='%1.1f%%',colors=color)
    plt.title('Porcentagem do tipo de entreterimento adicionado ao ano',fontsize=16)
    st.pyplot(fig2)

with tab3:
    fig3 = plt.figure(figsize=(14,7))
    sns.countplot(y=df['year_added'], order=df['year_added'].value_counts().index,palette='Set2')
    plt.title('Conteúdos que foram adicionados ao longo dos anos', fontsize=16)
    st.pyplot(fig3)

with tab4:
    fig4 = plt.figure(figsize=(14,7))
    sns.countplot(x=year['month_added'], palette='Set2')
    plt.title('Conteúdos que foram adicionados nos meses', fontsize=16)
    st.pyplot(fig4)

with tab5:
    fig5 = plt.figure(figsize=(14,7))
    sns.countplot(x=year['day_added'], palette='Set2')
    plt.title('Conteúdos que foram adicionados nos dias', fontsize=16)
    st.pyplot(fig5)

#? ----- gráficos solo ------
st.write('## Gráfico')
tab6, tab7, tab8, tab9 = st.tabs(['gráfico1','gráfico2','gráfico3','gráfico4'])

# Conteúdos adicionados ao longo dos anos
with tab6:

    tv = df[df['type']=='TV Show']
    movie = df[df['type'] == 'Movie']
    col = 'year_added'

    v1 = tv[col].value_counts().reset_index()
    v1 = v1.rename(columns= {col : 'count', 'index': col})
    v1['percent'] = v1['count'].apply(lambda x: 100*x/sum(v1['count']))
    v1 = v1.sort_values(col)

    v2 = movie[col].value_counts().reset_index()
    v2 = v2.rename(columns={col:'count', 'index':col})
    v2['percent'] = v2['count'].apply(lambda x: 100*x/sum(v2['count']))
    v2 = v2.sort_values(col)

    trace1 = go.Bar(x=v1[col], y=v1['count'], name='TV Shows', marker=dict(color='#00CED1'))

    trace2 = go.Bar(x=v2[col], y=v2['count'], name='Movies', marker=dict(color='#3CB371'))

    data = [trace1, trace2]

    layout = go.Layout(title='Conteúdos adicionados ao longo dos anos', legend=dict(x=0.1, y=1.1, orientation='h'))
    fig6 = go.Figure(data, layout=layout)
    st.plotly_chart(fig6)

with tab7:
    #  Ano de lançamento dos conteúdos
    col = 'release_year'

    v1 = tv[col].value_counts().reset_index()
    v1 = v1.rename(columns= {col : 'count', 'index': col})
    v1['percent'] = v1['count'].apply(lambda x: 100*x/sum(v1['count']))
    v1 = v1.sort_values(col)

    v2 = movie[col].value_counts().reset_index()
    v2 = v2.rename(columns={col:'count', 'index':col})
    v2['percent'] = v2['count'].apply(lambda x: 100*x/sum(v2['count']))
    v2 = v2.sort_values(col)

    trace1 = go.Bar(x=v1[col], y=v1['count'], name='TV Shows', marker=dict(color='#00CED1'))
    trace2 = go.Bar(x=v2[col], y=v2['count'], name='Movie', marker=dict(color='#3CB371'))

    data = [trace1, trace2]

    layout = go.Layout(title=' Ano de lançamento dos conteúdos', legend= dict(x=0.1, y=1.1, orientation='h'))
    fig7 = go.Figure(data, layout=layout)
    st.plotly_chart(fig7)

with tab8:
    # mês mais adicionado
    col = 'month_added'

    m1 = tv[col].value_counts().reset_index()
    m1 = m1.rename(columns={col:'count', 'index':col})
    m1['percent'] = m1['count'].apply(lambda x: 100*x/sum(m1['count']))
    m1 = m1.sort_values(col)

    m2 = movie[col].value_counts().reset_index()
    m2 = m2.rename(columns={col:'count', 'index':col})
    m2['percent'] = m2['count'].apply(lambda x: 100*x/sum(m2['count']))
    m2 = m2.sort_values(col)

    trace1 = go.Bar(x=m1[col], y=m1['count'], name='TV Show', marker=dict(color='#00CED1'))
    trace2 = go.Bar(x=m2[col], y=m2['count'], name='Movie', marker=dict(color='#3CB371'))

    data= [trace1, trace2]

    layout = go.Layout(title='Qual mês o conteúdo é mais adicionado?', legend=dict(x=0.1, y=1.1, orientation='h'))
    fig8 = go.Figure(data, layout=layout)
    st.plotly_chart(fig8)

with tab9:
    col = 'rating'

    c1 = tv[col].value_counts().reset_index()
    c1 = c1.rename(columns={col:'count', 'index':col})
    c1['percent'] = c1['count'].apply(lambda x: 100*x/sum(c1['count']))
    c1 = c1.sort_values(col)

    c2 = movie[col].value_counts().reset_index()
    c2 = c2.rename(columns={col:'count', 'index':col})
    c2['percent'] = c2['count'].apply(lambda x: 100*x/sum(c2['count']))
    c2 = c2.sort_values(col)

    trace1 = go.Bar(x=c1[col], y=c1['count'], name='TV Show', marker=dict(color='#00CED1'))
    trace2 = go.Bar(x=c2[col], y=c2['count'], name='Movies', marker=dict(color='#3CB371'))

    data = [trace1, trace2]

    layout = go.Layout(title='', legend=dict(x=0.1, y=1.1, orientation='h'))
    fig9 = go.Figure(data, layout=layout)
    layout = go.Layout(title='Avaliação por tipo de entreterimento', legend=dict(x=0.1, y=1.1, orientation='h'))
    st.plotly_chart(fig9)

st.title('Filmes adicionados e lançados nos EUA')
st.text('''Como os EUA é uma indústria cinematográfica, 
aqui abaixo vamos ver os conteúdos mais adicionados e lançados ao longo dos anos''')
# filtrando
us = df[df['country'] == 'United States']

tab10, tab11, tab12 = st.tabs(['gráfico10','gráfico11','gráfico12'])

with tab10:
    fig10 = plt.figure(figsize=(14,14))
    sns.countplot(y=us['release_year'], order=us['release_year'].value_counts().index)
    plt.title('Ano de Lançamento nos United State')
    st.pyplot(fig10)

with tab11:
    fig11 = plt.figure(figsize=(14,7))
    sns.countplot(x=us['year_added'])
    plt.title('Ano Adicionado nos United State')
    st.pyplot(fig11)

with tab12:
    fig12 = plt.figure(figsize=(14,7))
    sns.countplot(x=us['month_added'])
    plt.title('Ano Adicionado nos United State')
    st.pyplot(fig12)

st.write('## Tabela')
with st.expander('ANO DE LANÇAMENTO: 20 FILMES ANTIGOS DOS US.'):
    ano_usa_an = us[['title', 'release_year']].sort_values('release_year',ascending=True).head(20)
    st.write(ano_usa_an)

with st.expander( 'ANO DE LANÇAMENTO: 20 FILMES RECENTES DOS US'):
    ano_usa = us[['title', 'release_year']].sort_values('release_year',ascending=False).head(20)
    st.write(ano_usa)

with st.expander('DIRETORES MAIS ADICIONADOS'):
    diretor = us['director'].value_counts().reset_index().head(20)
    st.write(diretor)

with st.expander('QUAIS AS 20 CATEGORIAS MAIS ADICIONADAS?'):
    lista = us['listed_in'].value_counts().reset_index().head(20)
    st.write(lista)

st.title('Contagem de palavras')
# usando a função text_freq que faz a contagem de palavras dentro de uma coluna
categoria_lista = text_freq(df['listed_in'])
with st.expander('Frequência de palavras na coluna categoria de programas de TV'):
    st.write(categoria_lista)
    # nuvem de palavras
    texto = df['listed_in']
    text = list(set(texto))
    fig15 = plt.figure(figsize=(14,7))
    wordcloud = WordCloud(max_words=1000000, background_color='black').generate(str(text))

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(fig15)

with st.expander('Diretores mais frequentes'):
    diretor_freq = text_freq(df['director'])
    st.write(diretor_freq)

    # nuvem de palavras
    diretor = df['director']
    text = list(set(diretor))
    fig16 = plt.figure(figsize=(14,7))

    wordcloud = WordCloud(max_words=1000000, background_color='black').generate(str(text))

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(fig16)
    