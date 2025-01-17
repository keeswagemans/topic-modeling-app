import re
import pandas as pd
from nltk.corpus import stopwords
from itertools import chain 
import nltk
import spacy 
import json 

class Preprocess:
    
    def __init__(self, text_dict, language, custom_filterwords_path, custom_filterwords_list): 
        self.text_dict = text_dict 
        self.language = language 
        self.custom_filterwords_path = custom_filterwords_path
        self.custom_filterwords_list = custom_filterwords_list 

    def preprocessing(text_dict, language, custom_filterwords_path=None, custom_filterwords_list=None):
        """
        Preprocesses text data by performing several steps including cleaning, removing stopwords, 
        removing filter words, and lemmatization.

        Parameters:
        text_dict (dict): A dictionary where keys are document identifiers and values are strings of text.
        language (str): The language for stopwords removal.
        custom_filterwords_path (str, optional): Path to a TSV file containing filter words. Defaults to None.
        custom_filterwords_list (list, optional): A list of custom filter words. Defaults to None.

        Returns:
        dict: A dictionary where keys are document identifiers and values are lists of lemmatized words.
        """
        # Step 1: Clean text
        dictionary = {}
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        punctuation_pattern = r'[^\w\s-]'

        for key, value in text_dict.items():
            text_data_cleaned = []
            words = value.split()
            for word in words:
                word = re.sub(url_pattern, '', word)
                word = re.sub(punctuation_pattern, '', word)
                word = re.sub(r'\s-\s', ' ', word)
                word = word.strip()
                word = word.replace('\n\n', '').replace('\n', '')
                word = re.sub(r'[^a-zA-Z\s]', '', word)
                word = word.lower()

                if word:
                    text_data_cleaned.append(word)

            dictionary[key] = text_data_cleaned

        # Step 2: Remove stopwords
        nltk.download('stopwords')
        stop_words = stopwords.words(language)

        for key, value in dictionary.items():
            filtered_text = [word for word in value if word not in stop_words]
            dictionary[key] = filtered_text

        # Step 3: Remove filter words from TSV file
        if custom_filterwords_path:
            df_tsv = pd.read_csv(custom_filterwords_path, delimiter='\t', engine='python')
            filterwords = df_tsv[
                df_tsv['NOU-C(number=sg)'].str.contains(
                    "ADV|PD|COLL|AA|ADP|RES|INT|VRB|CONJ", 
                    case=False, na=False
                )
            ]['1 aprilmopje'].tolist()

            for key, value in dictionary.items():
                filtered_text = [word for word in value if word not in filterwords]
                dictionary[key] = filtered_text

        # Step 4: Remove custom filter words
        if custom_filterwords_list:
            for key, value in dictionary.items():
                custom_filter_words_text = [word for word in value if word not in custom_filterwords_list]
                dictionary[key] = custom_filter_words_text

        # Step 5: Lemmatization
        lemmatized_texts = {}
        nlp = spacy.load('nl_core_news_sm')

        for key, sentences in dictionary.items():
            lemmatized_sentences = []
            for doc in nlp.pipe(sentences, disable=["tagger", "parser", "ner", "textcat"]):
                lemmatized_sentences.append([token.lemma_ for token in doc])
            lemmatized_texts[key] = lemmatized_sentences

        for key, value in lemmatized_texts.items():
            new_value = list(chain(*value))
            lemmatized_texts[key] = new_value

        return lemmatized_texts

# Running the code 
input_data = json.load(open("extractedtext/extractedtext.json"))
data_preprocessed = Preprocess.preprocessing(input_data, language='dutch', custom_filterwords_path='molex/molex_22_02_2022.tsv', custom_filterwords_list=None)
json.dump(data_preprocessed, open("preprocessing/preprocessing.json", "w"))