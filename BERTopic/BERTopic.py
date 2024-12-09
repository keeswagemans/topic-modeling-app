import json 
from bertopic import BERTopic 
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer 

data = json.load(open("/content/drive/MyDrive/SZW/Latent_Dirichlet_Allocation/json/data_lemma_per_doc.json"))

