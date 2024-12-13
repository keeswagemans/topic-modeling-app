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
    def lda(data, corpus, save_path): 
        
        """
        This function trains an LDA model on the data and saves the model to the specified path. 
        
        """
        mdl = tp.LDAModel(tw=tp.TermWeight.ONE, min_cf=3, rm_top=5, k=5, corpus=corpus)
        for line in data:
            ch = line.strip().split()
            mdl.add_doc(ch)
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

data = json.load(open("topic-modeling-app/preprocessing/preprocessing.json"))
corpus = LDA.corpus(data)    
LDA.lda(data, corpus, "topic-modeling-app/models/lda_model.bin")




