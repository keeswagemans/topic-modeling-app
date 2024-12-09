import re
import pandas as pd
from nltk.corpus import stopwords
import nltk
import spacy 
import json 

class Preprocess:
    
    def __init__(self, input_data): 
        self.input_data = input_data

    def preprocessing(self, text_list):
        """
        Regular preprocessing steps for a list of strings.
        """
        dictionary = {}
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        punctuation_pattern = r'[^\w\s-]'

        for key, value in text_list.items():
            text_data_cleaned = []
            for text in value:
                text = re.sub(url_pattern, '', text)
                text = re.sub(punctuation_pattern, '', text)
                text = re.sub(r'\s-\s', ' ', text)
                text = text.strip()
                text = text.replace('\\n', '').replace('\n', '')
                text = re.sub(r'[^a-zA-Z\s]', '', text)
                text = text.lower()

                if text:
                    text_data_cleaned.append(text)

            dictionary[key] = text_data_cleaned

        return dictionary
    
    def remove_stopwords(self, text, language):
        """
        Removing stopwords from text.

        """
        dictionary = {}

        nltk.download('stopwords')
        stop_words = (stopwords.words(language))

        for key, value in text.items():
            filtered_text = []
            for word in value:
                if word not in stop_words:
                    filtered_text.append(word)

        dictionary[key] = filtered_text

        return dictionary
    
    def remove_filterwords(self, text):
        """
        Removing Dutch words.

        """
        dictionary = {}

        df_tsv = pd.read_csv('C:/Users/KWAGEMAN/Documents/LDA_App/topicmodelingapp/molex/molex_22_02_2022.tsv', delimiter='\t', engine='python')
        filterwords = df_tsv[df_tsv['NOU-C(number=sg)'].str.contains("ADV|PD|COLL|AA|ADP|RES|INT|NOU-P|NUM|VRB|CONJ", case=False, na=False)]['1 aprilmopje'].tolist()


        for key, value in text.items():
            filtered_text = []
            for word in value:
                if word not in filterwords:
                    filtered_text.append(word)

        dictionary[key] = filtered_text

        return dictionary 

    def remove_custom_filterwords(self, text, custom):
        """
        Removing custom filterwords.

        """
        dictionary = {}

        for key, value in text.items():
            custom_filter_words_text = []
            for word in value:
                if word not in custom:
                    custom_filter_words_text.append(word)

        dictionary[key] = custom_filter_words_text

        return dictionary
    
    def lemmatization(self, text):
        """
        Returns the lemmatized text for each key in the input dictionary.

        Args:
            text (Dict[str, List[str]]): A dictionary where the key is a string and the value is a list of strings.

        Returns:
            Dict[str, List[List[str]]]: A dictionary with the same keys, where each value is a list of lists of lemmatized tokens.
        """
        lemmatized_texts = {}
        nlp = spacy.load('nl_core_news_sm')

        for key, sentences in text.items():
            lemmatized_sentences = []
            for doc in nlp.pipe(sentences, disable=["tagger", "parser", "ner", "textcat"]):
                lemmatized_sentences.append([token.lemma_ for token in doc])
            lemmatized_texts[key] = lemmatized_sentences

        return lemmatized_texts


# Running the code 
input_data = json.load(open("C:/Users/KWAGEMAN/Documents/LDA_App/topicmodelingapp/extractedtext/extractedtext.json"))
instance = Preprocess(input_data)
data_preprocessed = instance.preprocessing(input_data)
data_stopwords_dutch = instance.remove_stopwords(input_data, 'dutch')
data_stopwords_english = instance.remove_stopwords(data_stopwords_dutch, 'english')
data_filterwords = instance.remove_filterwords(data_stopwords_english)
data_lemma = instance.lemmatization(data_filterwords)
json.dump(data_lemma, open("C:/Users/KWAGEMAN/Documents/LDA_App/topicmodelingapp/preprocessing/preprocessing.json", "w"))