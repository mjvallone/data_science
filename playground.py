import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from functools import reduce


st.title("Playing with Pandas")

@st.cache
def load_data(allow_output_mutation=True):
  ## Cosas por las que pase:
  # df3 no tenia en el primer lugar los titulos de las columnas
  # al sumar los df lo hace posicionalmente, considerar que pueden no estar ordenados con el mismo criterio!
  # luego de ordenar, resetear los index porque ESO es lo que usa para las operaciones

  df1 = pd.read_csv("https://datos.mininterior.gob.ar/dataset/dd032084-b7eb-4317-9151-05fc850c1654/resource/47b78cd9-f8a0-4e05-8088-35051e8fbb0a/download/residencias-otorgadas---1-trimestre---ano-2019.csv").sort_values('PROVINCIA').reset_index()
  df2 = pd.read_csv("https://datos.mininterior.gob.ar/dataset/dd032084-b7eb-4317-9151-05fc850c1654/resource/e14d00b5-5bd5-4bfe-b608-315c1a615aa8/download/residencias-otorgadas---2-trimestre---ano-2019.csv").sort_values('PROVINCIA').reset_index()
  df3 = pd.read_csv("https://datos.mininterior.gob.ar/dataset/dd032084-b7eb-4317-9151-05fc850c1654/resource/244f6f18-ab64-4969-b7d3-49e3de9cf758/download/residencias-otorgadas---3-trimestre---ano-2019.csv", names=['PROVINCIA', 'TRANSITORIAS', 'TEMPORARIAS', 'PERMANENTES', 'TOTAL']).sort_values('PROVINCIA').reset_index()
  df4 = pd.read_csv("https://datos.mininterior.gob.ar/dataset/dd032084-b7eb-4317-9151-05fc850c1654/resource/99d4492d-9787-4afd-8784-3d02635b58a5/download/residencias-otorgadas---4-trimestre---ano-2019.csv").sort_values('PROVINCIA').reset_index()

  given_residences = df1.copy()
  given_residences['TRANSITORIAS'] = df1['TRANSITORIAS'] + df2['TRANSITORIAS'] + df3['TRANSITORIAS'] + df4['TRANSITORIAS']
  given_residences['TEMPORARIAS'] = df1['TEMPORARIAS'] + df2['TEMPORARIAS'] + df3['TEMPORARIAS'] + df4['TEMPORARIAS']
  given_residences['PERMANENTES'] = df1['PERMANENTES'] + df2['PERMANENTES'] + df3['PERMANENTES'] + df4['PERMANENTES']
  given_residences['TOTAL'] = df1['TOTAL'] + df2['TOTAL'] + df3['TOTAL'] + df4['TOTAL']

  return given_residences

data_load_state = st.empty()
data_load_state.text('Loading data...')
data = load_data()
data_load_state.text('Loading data... done!')
st.write(data)
provinces = data.loc[:,'PROVINCIA']
transitory = data.loc[:,'TRANSITORIAS']
temporary = data.loc[:,'TEMPORARIAS']
permanent = data.loc[:,'PERMANENTES']
totals = data.loc[:,'TOTAL']
df_totals = pd.DataFrame({'provinces':provinces, 'totals':totals})

def show_seaborn_bar_plot():
  sns.set(style="whitegrid")
  f, ax = plt.subplots(figsize=(7, 12))

  sns.set_color_codes("pastel")
  chart = sns.barplot(x=provinces, y=transitory, label="Transitory", data=df_totals, color="b")

  sns.set_color_codes("muted")
  chart = sns.barplot(x=provinces, y=temporary, label="Temporary", data=df_totals, color="g")

  sns.set_color_codes("muted")
  chart = sns.barplot(x=provinces, y=permanent, label="Permanent", data=df_totals, color="r")

  ax.legend(ncol=2, loc="lower right", frameon=True)
  chart.set_xticklabels(chart.get_xticklabels(), rotation=45, horizontalalignment='right')
  ax.set(ylabel="", xlabel="Provinces")
  plt.title("Total Residences Argentina 2019")
  st.pyplot()

show_seaborn_bar_plot()
