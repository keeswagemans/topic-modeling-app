import json  
from bertopic import BERTopic 


class BERTopic: 
    
    @staticmethod 
    def bertopic(data): 
        
        """
        This function creates a BERTopic object from the data.
        
        """
        
        model = BERTopic()
        topics, probs = model.fit_transform(data)
        
        return model, topics, probs 
    
    
dictionary = json.load(open("preprocessing/preprocessing.json")) 
data = dictionary.values()
data = [item for sublist in data for item in sublist]   
model, topics, probs = BERTopic.bertopic(data)    
    
