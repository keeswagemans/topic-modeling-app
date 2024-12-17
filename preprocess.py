import re
import pandas as pd
from nltk.corpus import stopwords
from itertools import chain 
import nltk
import spacy 
import json 

class Preprocess:

    @staticmethod
    def preprocessing(text_dict):
        """
        Regular preprocessing steps for a list of strings.

        """
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

        return dictionary

    @staticmethod
    def remove_stopwords(text, language):
        """
        Removing stopwords from text.
        """
        dictionary = {}

        nltk.download('stopwords')
        stop_words = stopwords.words(language)

        for key, value in text.items():
            filtered_text = []
            for word in value:
                if word not in stop_words:
                    filtered_text.append(word)

            dictionary[key] = filtered_text

        return dictionary

    @staticmethod
    def remove_filterwords(text):
        """
        Removing Dutch words based on a predefined filter list.
        """
        dictionary = {}

        df_tsv = pd.read_csv(
            'molex/molex_22_02_2022.tsv',
            delimiter='\t', engine='python'
        )
        filterwords = df_tsv[
            df_tsv['NOU-C(number=sg)'].str.contains(
                "ADV|PD|COLL|AA|ADP|RES|INT|VRB|CONJ", 
                case=False, na=False
            )
        ]['1 aprilmopje'].tolist()

        for key, value in text.items():
            filtered_text = []
            for word in value:
                if word not in filterwords:
                    filtered_text.append(word)

            dictionary[key] = filtered_text

        return dictionary

    @staticmethod
    def remove_custom_filterwords(text, custom):
        """
        Removing custom filter words.
        """
        dictionary = {}

        for key, value in text.items():
            custom_filter_words_text = []
            for word in value:
                if word not in custom:
                    custom_filter_words_text.append(word)

            dictionary[key] = custom_filter_words_text

        return dictionary

    @staticmethod
    def lemmatization(text):
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

        for key, value in lemmatized_texts.items(): 
            new_value = list(chain(*value))
            lemmatized_texts[key] = new_value 

        return lemmatized_texts


# Running the code 
input_data = json.load(open("extractedtext/extractedtext.json"))
data_preprocessed = Preprocess.preprocessing(input_data)
data_stopwords_dutch = Preprocess.remove_stopwords(data_preprocessed, 'dutch')
data_stopwords_english = Preprocess.remove_stopwords(data_stopwords_dutch, 'english')
data_filterwords = Preprocess.remove_filterwords(data_stopwords_english)
data_lemma = Preprocess.lemmatization(data_filterwords)
json.dump(data_lemma, open("preprocessing/preprocessing.json", "w"))
