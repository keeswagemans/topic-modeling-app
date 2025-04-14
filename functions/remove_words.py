import json 

class Remove_Words: 
    
    @staticmethod 
    def remove_words(text, words): 
        
        dictionary = {}
        
        for key, value in text.items():  
            filtered_text = []
            for word in value: 
                if word not in words: 
                    filtered_text.append(word)
                    
            dictionary[key] = filtered_text
        
        return dictionary 

words_to_remove = json.load(open('preprocessing/words_to_remove.json')) 
data = json.load(open('preprocessing/preprocessing.json'))
remove_words = Remove_Words.remove_words(data, words_to_remove) 
json.dump(remove_words, open('preprocessing/preprocessing.json', 'w')) 