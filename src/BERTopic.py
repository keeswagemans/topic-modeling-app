from bertopic import BERTopic 
import json 

dictionary = json.load(open("preprocessing/preprocessing.json"))
data = list(dictionary.values())     
final_data = [item for sublist in data for item in sublist]  

model = BERTopic(language="dutch", calculate_probabilities=True)   
topics, _ = model.fit_transform(final_data)  
model.save("models/bertopic_model")     
result = model.visualize_topics() 
result_barchart = model.visualize_barchart() 
print(result_barchart) 
