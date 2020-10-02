import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import urllib.request, json 
from pandas.io.json import json_normalize


st.title("Playing with COOBS data")

dev_url = "http://localhost:8000/api/public-actions?format=json"
prod_url = "https://coobs.io/api/public-actions?format=json"

def load_data():
  with urllib.request.urlopen(dev_url) as url:
    data = json.loads(url.read().decode())
    return data

def show_bar_plot(actionsByPrinciplesData, principles):
  sns.set(style="whitegrid")
  f, ax = plt.subplots(figsize=(12,12))
  principles_names = principles['name']
  totals = actionsByPrinciplesData['total']
  df_actions = pd.DataFrame({'principles': principles_names, 'totals':totals})
  
  sns.set_color_codes("pastel")
  chart = sns.barplot(x=principles_names, y=totals, data=df_actions, color="b")

  ax.legend(ncol=2, loc="lower right", frameon=True)
  chart.set_xticklabels(chart.get_xticklabels(), rotation=20, horizontalalignment='right', size=9)
  ax.set(ylabel="Actions", xlabel="Principles")
  plt.title("Actions by principles")
  st.pyplot()

data_load_state = st.empty()
data_load_state.text('Loading data...')
data = load_data()
data_load_state.text('Loading data... done!')
# st.write("Actions by Principles for current year")
# st.write(data["allActionsByPrinciplesData"])

allActionsByPrinciplesData = json_normalize(data["actionsByPrinciplesData"])
principles = json_normalize(data["principles"])
actions = json_normalize(data["actions"])
cooperatives = json_normalize(data["cooperatives"])

# st.write("All principles")
# st.write(data["principles"])

# show_bar_plot(allActionsByPrinciplesData, principles)

st.write("Fiqus actions")
fiqus_actions = actions[actions["cooperative"] == 2]
# st.write(fiqus_actions)
df = dict()
for i  in range(0, len(fiqus_actions)):
  action = fiqus_actions.iloc[i]
  for principle in action["principles"]:
    try:
      df[principle["name"]] = df[principle["name"]] + 1
    except:
      df[principle["name"]] = 1
# st.write(df.keys())

sns.set(style="whitegrid")
f, ax = plt.subplots(figsize=(12,12))
principles_names = df.keys()
totals = df.values()
# st.write(principles_names)
# st.write(totals)
df_actions = pd.DataFrame({'principles': principles_names, 'totals':totals})

sns.set_color_codes("pastel")
chart = sns.barplot(x=principles_names, y=totals, data=df_actions, color="b")

ax.legend(ncol=2, loc="lower right", frameon=True)
chart.set_xticklabels(chart.get_xticklabels(), rotation=20, horizontalalignment='right', size=9)
ax.set(ylabel="Actions", xlabel="Principles")
plt.title("Actions by principles")
st.pyplot()


# st.write("Actions for current year")
# st.write(data["actions"])