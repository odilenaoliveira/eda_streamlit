from collections import Counter
import pandas as pd
import numpy as np

def loadData():
    df = pd.read_csv('netflix1.csv')
    # Transformando as datas
    df['date_added'] = pd.to_datetime(df['date_added'])
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    df['day_added'] = df['date_added'].dt.day

    df['min']=df['duration'].fillna('0')
    df['min']=df['min'].str.replace(' min','')
    df['min']=df['min'].str.replace(' Season','')
    df['min']=df['min'].str.replace(' Seasons','')
    df['min']=df['min'].str.replace('s','')
    df['min']=df['min'].astype(str).astype(int)
    df = df.copy()
    return df

def features(df):
    features = ['title', 'duration']
    durations = df[features]

    durations['number_of_seasons'] = durations['duration'].str.replace(' Seasons', '')
    durations['number_of_seasons'] = durations['number_of_seasons'].str.replace(' Season', '')
    durations['number_of_seasons'] = durations['number_of_seasons'].str.replace(' min', '678')
    durations['number_of_seasons']= durations['number_of_seasons'].astype(str).astype(int)  
    durations = durations.copy()
    return durations

def text_freq(data):
  tipo = list(data)
  gen = []

  for i in tipo:
      i = list(i.split(','))
      for j in i:
          gen.append(j.replace(' ',''))
  genero = Counter(gen)
  tabela = pd.DataFrame({'Words':genero.keys(), 'Count':genero.values()}).sort_values('Count', ascending=False)
  tabela = tabela.reset_index()
  tabela = tabela.drop('index',axis=1)
  return tabela