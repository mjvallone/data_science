import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


try:
    from urllib.request import Request, urlopen  # Python 3
except ImportError:
    from urllib2 import Request, urlopen  # Python 2

def get_data_from_url(url):
  req = Request(url)
  req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0')
  content = urlopen(req)
  df = pd.read_csv(content, encoding="ISO-8859-1")
  df.to_csv('filename.csv', encoding='utf-8')

  return pd.read_csv("filename.csv", index_col=1).fillna(0).iloc[:, 1:]
  # d = pd.read_csv("filename.csv", index_col=0)
  # st.write(d)
  # return d


@st.cache
def load_data(allow_output_mutation=True):
  desempleo_2018 = get_data_from_url("https://datos.mardelplata.gob.ar/sites/default/files/tasa-desocupacion-2018.csv")
  empleo_2018 = get_data_from_url("https://datos.mardelplata.gob.ar/sites/default/files/tasa-empleo-2018.csv")
  actividad_2018 = get_data_from_url("https://datos.mardelplata.gob.ar/sites/default/files/tasa-actividad-2018.csv")

  return [desempleo_2018, empleo_2018, actividad_2018]

def split_summary_detail(df):
  resumen = df.iloc[0:3, :]
  detalle = df.iloc[3:, :]
  resumen = resumen.T
  detalle = detalle.T
  resumen.columns = [col.replace("ó", "o") if col.find("ó") != -1 else col for col in resumen.columns]
  detalle.columns = [col.replace("ñ", "n") if col.find("ñ") != -1 else col for col in detalle.columns]
  return [resumen, detalle]

def graph(df):
  sns.set(style="whitegrid")
  sns.lineplot(data=df)
  plt.legend(loc='upper left')
  plt.ylabel("Tasa %")
  st.pyplot()  


st.title("Empleo Mar del Plata 2018")
st.write("""
## Tasa de desempleo
# """)
[desempleo_2018, empleo_2018, actividad_2018] = load_data()
[resumen_des, detalle_des] = split_summary_detail(desempleo_2018)
# st.write(desempleo_2018)
# st.write(resumen_des)
# st.write(detalle_des)
graph(resumen_des)
graph(detalle_des)

## TODO podría comparar la info de 2018 y 2019 en 2 graficos que se muestren en paralelo - usar matplotlib

st.write("Tasa de empleo")
[resumen_emp, detalle_emp] = split_summary_detail(empleo_2018)
# st.write(empleo_2018)
# st.write(resumen_emp)
# graph(resumen_emp)
# st.write(detalle_emp)
# graph(detalle_emp)

# st.write("Tasa de actividad")
# st.write(actividad_2018)