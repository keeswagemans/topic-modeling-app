import sys 
import json
import pandas as pd 
import numpy as np 
import tomotopy as tp 
import os 

class LDA: 
    
    @staticmethod 
    def corpus(data): 
        
        """
        This function creates a corpus object from the data.
        
        """
        
        corpus = tp.utils.Corpus(tokenizer=tp.utils.SimpleTokenizer())
        corpus.process(data)
        
        return corpus 
    
    @staticmethod 
    def lda(input_dict, corpus, save_path): 
        
        """
        This function trains an LDA model on the data and saves the model to the specified path. 
        
        """
        mdl = tp.LDAModel(tw=tp.TermWeight.ONE, min_cf=3, rm_top=5, k=5, corpus=corpus)
        
        for pdf, words in input_dict.items():
            mdl.add_doc(words)   
        
        mdl.burn_in = 100
        mdl.train(0)
        print("Len:", len(mdl.docs), ", Vocab size:", len(mdl.used_vocabs), ", Num words:", mdl.num_words)
        print("Removed top words:", mdl.removed_top_words)
        print("Training...", file=sys.stderr, flush=True)
        mdl.train(10000, show_progress=True)
        mdl.summary()
        print("Saving...", file=sys.stderr, flush=True)
        mdl.save(save_path, True)

        for k in range(mdl.k):
            print("Topic #{}".format(k))
            for word, prob in mdl.get_topic_words(k):
                print("\t", word, prob, sep = "\t")
                
        # Print topic distribution and words for each document
        for i, doc in enumerate(mdl.docs):
            if i < len(input_dict):
                pdf_name = list(input_dict.keys())[i]
                topic_dist = doc.get_topic_dist()
                dominant_topic = topic_dist.argmax()
                topic_words = mdl.get_topic_words(dominant_topic)
                print(f"Document {i} ({pdf_name}):")
                print(f"Dominant Topic Words: {topic_words}")

dictionary = json.load(open("preprocessing/preprocessing.json"))
data = dictionary.values()
final_data = [item for sublist in data for item in sublist]
corpus = LDA.corpus(final_data)   
corpus.save("models/corpus.cps") 
LDA.lda(dictionary, corpus, "models/lda_model.bin")




