import streamlit as st
import pandas as pd
import json
import config
import time
from pandas.io.json import json_normalize

CHANNEL_ID = "UCoGBPBXyq28cE4g2TaB6lRQ"  #DamianKucOK
VIDEO_ID = "RHlFYRonmj4"  #Shoko Asahara
MAX_RESULTS = 10
YOUTUBE_BASE_API_URL = "https://www.googleapis.com/youtube/v3/"

# videos_list = "https://www.googleapis.com/youtube/v3/search?key=AIzaSyCuCqi6DNPjWgpsRnsRUtDlr0NpvMOJNuc&textFormat=plainText&channelId=UCoGBPBXyq28cE4g2TaB6lRQ&part=snippet,id&order=date&maxResults=50"

# channel_uploads_data.json = "https://www.googleapis.com/youtube/v3/channels?key=AIzaSyCuCqi6DNPjWgpsRnsRUtDlr0NpvMOJNuc&part=contentDetails&id=UCoGBPBXyq28cE4g2TaB6lRQ"
# channel_videos_list_data.json = "https://www.googleapis.com/youtube/v3/playlistItems?playlistId=UUoGBPBXyq28cE4g2TaB6lRQ&key=AIzaSyCuCqi6DNPjWgpsRnsRUtDlr0NpvMOJNuc&part=snippet&maxResults=50"

# comments_data.json = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet,replies&allThreadsRelatedToChannelId=UCoGBPBXyq28cE4g2TaB6lRQ&key=AIzaSyCuCqi6DNPjWgpsRnsRUtDlr0NpvMOJNuc&maxResults=100&order=time"
# comments de canal (canal y videos) = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet,replies&allThreadsRelatedToChannelId={CHANNEL_ID}&key={API_KEY}&maxResults=100&order=time"
# con nextPageToken puedo obtener los resultados de la prox pag, mandarlo como param en pageToken

# endpoints youtube api https://stackoverflow.com/questions/18953499/youtube-api-to-fetch-all-videos-on-a-channel

#QURTSl9pMkR3VTlPeEVvcjB1TVhEYTFxcW4wTFZMS1A4XzRxSm5qamk5d3BZc2ptOUhEZ19lVXJISUd4eWxWR3MzVV9iUlUwSjlydXFBV1BGd0FGbWtsSmg3YzN4dkY2dG9oN244VjNlNlVMSFZLOEd4UGg0eXlyOWlQVV90WXhtcXI3b1VVaHlVM3BIVE4wd1dUSmRjS1VXTDV0WEdyWjRDOG9TM29keWQyT1RXdV93TXNKa0NzT2RBQXhQMURVWjdWaG53

try:
    from urllib.request import Request, urlopen  # Python 3
except ImportError:
    from urllib2 import Request, urlopen  # Python 2

#@st.cache
def get_data_into_file(filename):
  url = YOUTUBE_BASE_API_URL+"commentThreads?key={}&textFormat=plainText&part=snippet&videoId={}&maxResults={}".format(config.API_KEY, VIDEO_ID, MAX_RESULTS)
  response = urlopen(url)
  json_data = response.read().decode('utf-8', 'replace')
  import pdb; pdb.set_trace()
  data = json.loads(json_data)['items']
  json_data = json_normalize(data)

  with open(filename, 'w') as outfile:
      json.dump(json_data, outfile)  

def load_data_from(filename):
  with open(filename) as json_file:
      data = json.load(json_file)['items']
      comments = []
      for item in data:
        comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
        comments.append(comment)
      
      return pd.Series(comments)


st.title("Comentarios de videos")
#get_data_into_file("data.json")
#comments_video = load_data_from("data/video_data.json")
#st.write(comments_video)
placeholder = st.empty()
placeholder.text("Cargando comentarios")
last_1000_comments = pd.Series()
for i in range(10):
  placeholder.text("Cargando {}%".format((i+1)*10))
  #st.write("Processing: data/comments_data_{}.json".format(i))
  last_1000_comments = last_1000_comments.append(load_data_from("data/comments_data_{}.json".format(i)), ignore_index=True)

st.success("{} comentarios agregados".format(len(last_1000_comments)))
placeholder.empty()
st.write(last_1000_comments)