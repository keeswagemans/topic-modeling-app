import sys 
import json
import pandas as pd 
import numpy as np 
import tomotopy as tp 
import json    

# Import variables 
parameters = json.load(open("parameters/parameters.json")) 
min_cf = parameters["min_cf"]
min_df = parameters["min_df"]
top_words = parameters["top_words"]
number_topics = parameters["number_topics"]
alpha_raw = parameters["alpha_input"]
eta = parameters["eta"]

def change_alpha(alpha_raw): 
    if "," in alpha_raw: 
        alpha = [float(x.strip()) for x in alpha_raw.split(",")]
    else:
        alpha = float(alpha_raw)
    return alpha 

alpha = change_alpha(alpha_raw)

class LDA: 
    
    def __init__(self, data, min_cf, min_df, top_words, number_topics, alpha, eta):
        self.data = data  
        self.min_cf = min_cf 
        self.min_df = min_df
        self.top_words = top_words 
        self.number_topics = number_topics
        self.alpha = alpha 
        self.eta = eta 
        
    def corpus(data): 
        """
        Creates a corpus object from the provided data.

        This function initializes a corpus object using the `Corpus` class from the `tp.utils` module,
        with a simple tokenizer. It then processes the input data to populate the corpus with tokens.

        Parameters:
        data (str): The input data to be tokenized and added to the corpus.

        Returns:
        tp.utils.Corpus: A corpus object containing the tokenized data.
        """
        corpus = tp.utils.Corpus(tokenizer=tp.utils.SimpleTokenizer())
        corpus.process(data)
        
        return corpus 
    
    def lda(input_dict, corpus, save_path, min_cf, min_df, top_words, number_topics, alpha, eta): 
        """
        Trains an LDA model on the provided data and saves the model to the specified path.

        This function initializes and trains a Latent Dirichlet Allocation (LDA) model using the `tomotopy` library.
        It processes the input data, adds documents to the model, and trains the model. The trained model is then saved
        to the specified path. Additionally, the function prints various details about the model and the training process,
        including the number of documents, vocabulary size, and the number of words. It also prints the top words for each topic
        and the topic distribution for each document.

        Parameters:
        input_dict (dict): A dictionary where keys are document identifiers and values are lists of words in the documents.
        corpus (tp.utils.Corpus): A corpus object containing the tokenized data.
        save_path (str): The path where the trained model will be saved.
        min_cf (int): The minimum collection frequency of words to be included in the model.
        min_df (int): The minimum document frequency of words to be included in the model.
        top_words (int): The number of top words to be removed from the model.
        number_topics (int): The number of topics to be generated by the model.
        alpha (float): The hyperparameter for the document-topic distribution.
        eta (float): The hyperparameter for the topic-word distribution.

        Returns:
        None
        """  
        mdl = tp.LDAModel(tw=tp.TermWeight.ONE, min_cf=min_cf, min_df=min_df, rm_top=top_words, k=number_topics, alpha=alpha, eta=eta, corpus=corpus) 
        
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
LDA.lda(dictionary, corpus, "models/lda_model.bin", min_cf, min_df, top_words, number_topics, alpha, eta)
print(number_topics)