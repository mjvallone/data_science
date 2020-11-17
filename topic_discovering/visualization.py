# Execution of several models to compare the coherence value
import time
import matplotlib.pyplot as plt
from coherence_computation import *
# Execution of several models to compare the coherence value
start_time = time.time()

model_list, coherence_values = compute_coherence_values(dictionary=dictionary, corpus=corpus, texts=text_data, start=2, limit=50, step=6)
st.write("--- %s seconds for compute_coherence_values ---" % (time.time() - start_time))
get_ipython().run_line_magic('matplotlib', 'inline')