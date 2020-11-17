import gensim
import time
from gensim.models.coherencemodel import CoherenceModel

def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
  """
    Compute c_v coherence for various number of topics
    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics
    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective
    number of topics
  """
  coherence_values = []
  model_list = []
  for num_topics in range(start, limit, step):
    #the random_state parameter is fundamental if you want to reproduce the training run, its like a random seed
    s_time = time.time()
    model = gensim.models.ldamodel.LdaModel(corpus, num_topics = num_topics,
    id2word=dictionary, passes=15, random_state=1)
    print("--- "+str(time.time() - s_time)+" seconds for model with k = "+str(num_topics)+" ---")
    model_list.append(model)
    coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
    coherence_values.append(coherencemodel.get_coherence())
  
  return model_list, coherence_values