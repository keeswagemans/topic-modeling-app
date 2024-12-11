import json 
from bertopic import BERTopic
from bertopic import fit_transform  
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer 
from bertopic.representation import KeyBERTInspired 
from umap import UMAP 
from sklearn.decomposition import PCA 

sentence_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state=42)

class BERTopic: 

    @staticmethod
    def bertopic_model(data):
        topic_model = BERTopic()
        data_bertopic = ""
        for key, value in data.items(): 
            for word in value: 
                data_bertopic += word + " "
        print(data_bertopic)
        embeddings = sentence_model.encode(data_bertopic, show_progress_bar=True) 
        topics, probs = topic_model.fit_transform(data_bertopic, embeddings=embeddings) 
        topic_model.save("C:/Users/KWAGEMAN/Documents/LDA_App/topicmodelingapp/model/BERTopic")
        return topic_model, topics, probs 
    
# Running the model 
data = json.load(open("C:/Users/KWAGEMAN/Documents/LDA_App/topicmodelingapp/preprocessing/preprocessing.json"))
topic_model, _, _ = BERTopic.bertopic_model(data)
_, topics, probs = BERTopic.bertopic_model(data)


    


    







