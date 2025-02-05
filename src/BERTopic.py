from bertopic import BERTopic 
from sentence_transformers import SentenceTransformer 
from langchain.chat_models import AzureChatOpenAI 
import json 
import os  
import openai 

dictionary = json.load(open("preprocessing/preprocessing.json"))
data = list(dictionary.values())     
final_data = [item for sublist in data for item in sublist] 
language = "dutch"
calculate_probabilities = True   
embedding_model = SentenceTransformer("wietsedv/bert-base-dutch-cased") 
embedding_model2 = SentenceTransformer("DTAI-KULeuven/robbert-v2-dutch-sentiment") 

# class BERTopic: 
#     def __init__(self, embedding_model=None): 
#         self.model = BERTopic(embedding_model=embedding_model)
        
#     def fit_transform(final_data):
              
#         # Run model 
#         model = BERTopic(language=language, calculate_probabilities=calculate_probabilities, embedding_model=embedding_model) 
#         topics, probs = model.fit_transform(final_data) 
        
#         # Save model 
#         if "model/bertopic_model": 
#             os.remove("model/bertopic_model") 
#             model.save("models/bertopic_model", serialization="pytorch", save_ctfidf=True)   
#         else: 
#             model.save("models/bertopic_model", serialization="pytorch", save_ctfidf=True) 
           
#         # Return results   
#         return topics, probs     


# # Retrieve results 
# topics, probs = BERTopic.fit_transform(final_data)   
# print(topics) 
# print(probs)

############################################################## 
##             BERTOPIC WITH AZURE OPEN AI API              ##

# api_type = "azure" 
# api_key = "ChciroJAUkT4AOFa7GOu9RaXxvwPdFQHkbaAJ8La5ObUTuBhvJNTJQQJ99AKACYeBjFXJ3w3AAAAACOGphGX" 
# azure_endpoint = "https://premi0648592--openai.cognitiveservices.azure.com/openai/deployments/gpt-4o-szw/chat/completions?api-version=2024-08-01-preview" 
# api_version = "2024-10-01-preview" 
# deployment_name = "gpt-4o-szw" 

# # OpenAI API 
# prompt = "Genereer 20 topics uit de documenten."
# client = openai.OpenAI(api_key=api_key)
# representation_model = AzureChatOpenAI(api_type=api_type, 
#                                        api_key=api_key, 
#                                        azure_endpoint=azure_endpoint, 
#                                        api_version=api_version, 
#                                        deployment_name=deployment_name)  

# model = BERTopic(representation_model=representation_model)     
# topics, probs = model.fit_transform(final_data)  
# print(topics)   
# print(probs) 

# if "models/bertopic_model": 
#     os.remove("models/bertopic_model")   
#     model.save("models/bertopic_model", 
#            serialization="pytorch", 
#            save_ctfidf=True)
# else: 
#     model.save("models/bertopic_model", 
#             serialization="pytorch", 
#             save_ctfidf=True)     

# Run model 
model = BERTopic(language="dutch", calculate_probabilities=True, embedding_model=embedding_model) 
topics, probs = model.fit_transform(final_data) 

# Results 
print(topics)
print(probs)     

# Save model 
if "model/bertopic_model": 
    os.remove("models/bertopic_model") 
    model.save("models/bertopic_model", serialization="pytorch", save_ctfidf=True)   
else: 
    model.save("models/bertopic_model", serialization="pytorch", save_ctfidf=True) 
