import streamlit as st
import pandas as pd
import requests
import json

VIDEO_ID = "RHlFYRonmj4"
MAX_RESULTS=5
#url = "https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyCuCqi6DNPjWgpsRnsRUtDlr0NpvMOJNuc&textFormat=plainText&part=snippet&videoId=RHlFYRonmj4&maxResults=50"

try:
    from urllib.request import Request, urlopen  # Python 3
except ImportError:
    from urllib2 import Request, urlopen  # Python 2

def get_data_from_url(url):
  req = Request(url)
  req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0')
  content = urlopen(req)
  df = pd.read_json(content)

  return df


#@st.cache
def load_data(allow_output_mutation=True):
  from pandas.io.json import json_normalize

  url = "https://www.googleapis.com/youtube/v3/commentThreads?key={}&textFormat=plainText&part=snippet&videoId={}&maxResults={}".format(API_KEY, VIDEO_ID, MAX_RESULTS)
  response = urlopen(url)
  json_data = response.read().decode('utf-8', 'replace')
  d = json.loads(json_data)['items']
  data = d #pd.DataFrame.from_dict(d)
  return data


st.title("Comentarios de video")
comentarios = load_data()
st.write(comentarios)