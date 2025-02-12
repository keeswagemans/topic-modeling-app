from bertopic import BERTopic 
from sentence_transformers import SentenceTransformer 
import json 
import shutil 

dictionary = json.load(open("preprocessing/preprocessing.json"))
data = list(dictionary.values())     
final_data = [item for sublist in data for item in sublist] 
language = "dutch"
calculate_probabilities = True   
embedding_model = SentenceTransformer("wietsedv/bert-base-dutch-cased") 

# Run model 
model = BERTopic(language="dutch", calculate_probabilities=True, embedding_model=embedding_model) 
topics, probs = model.fit_transform(final_data)


# Results 
for num in range(0, 20): 
    words = model.get_topic(num) 
    print(f"Topic {num}: {words}") 


# Save model 
if "models/bertopic_model" == True: 
    shutil.rmtree("models/bertopic_model") 
    model.save("models/bertopic_model", serialization="pytorch", save_ctfidf=True)   
else:
    model.save("models/bertopic_model", serialization="pytorch", save_ctfidf=True) 
    
