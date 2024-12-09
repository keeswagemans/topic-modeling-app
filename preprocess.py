import re
import pandas as pd
from nltk.corpus import stopwords
import nltk

class Preprocess:
    
    def __init__(self, input_data, output_data): 
        self.input_data = input_data
        self.output_data = output_data

    def preprocess(self, text_data, language=None, custom_stopwords=None, use_filterwords=False, filterword_path=None):
        """
        General preprocessing function for text data.

        This function includes:
        - Cleaning text (removing URLs, punctuation, extra spaces, etc.)
        - Removing stopwords (default or language-specific)
        - Removing custom filter words
        - Removing filter words from a TSV file (if specified)

        Args:
            text_data (dict): Dictionary of text data to preprocess.
            language (str, optional): Language for stopwords. Defaults to None.
            custom_stopwords (list, optional): Custom stopwords to remove. Defaults to None.
            use_filterwords (bool, optional): If True, removes filter words from a TSV file. Defaults to False.
            filterword_path (str, optional): Path to the TSV file containing filter words. Defaults to None.

        Returns:
            dict: Preprocessed text data.
        """
        dictionary = {}
        url_pattern = re.compile(r"https?://\S+www\.\S+")
        punctuation_pattern = r'[^\w\s-]'
        
        # Load filter words if needed
        filterwords = []
        if use_filterwords and filterword_path:
            df_tsv = pd.read_csv(filterword_path, delimiter='\t', engine='python')
            filterwords = df_tsv[
                df_tsv['NOU-C(number=sg)'].str.contains(
                    "ADV|PD|COLL|AA|ADP|RES|INT|NOU-P|NUM|VRB|CONJ", case=False, na=False
                )
            ]['1 aprilmopje'].tolist()

        # Download stopwords if language is specified
        if language:
            nltk.download('stopwords')
            stop_words = set(stopwords.words(language))
        else:
            stop_words = set()

        # Preprocess text
        for key, value in text_data.items():
            processed_text = []
            for text in value:
                # Text cleaning
                text = re.sub(url_pattern, '', text)
                text = re.sub(punctuation_pattern, '', text)
                text = re.sub(r'\s-\s', ' ', text)
                text = text.strip()
                text = text.replace('\\n', '').replace('\n', '')
                text = re.sub(r'[^a-zA-Z\s]', '', text)
                text = text.lower()

                if text:
                    words = text.split()

                    # Remove stopwords
                    if stop_words:
                        words = [word for word in words if word not in stop_words]

                    # Remove custom stopwords
                    if custom_stopwords:
                        words = [word for word in words if word not in custom_stopwords]

                    # Remove filter words from TSV
                    if use_filterwords:
                        words = [word for word in words if word not in filterwords]

                    processed_text.extend(words)

            dictionary[key] = processed_text

        return dictionary

    def lemmatization(self, text: Dict[str, List[str]]) -> Dict[str, List[List[str]]]: 

        """
        
        Returns the lemmatized text for each key in the input dictionary. 

        Args:
        text (Dict[str, List[str]]): A dictionary where the key is a string and the value is a list of strings.

        Returns:
        Dict[str, List[List[str]]]: A dictionary with the same keys, where each value is a list of lists of lemmatized tokens.
        
        """

        lemmatized_text = {}
        nlp = spacy.load('nl_core_news_sm')

        for key, sentences in text.items(): 
            lemmatized_sentences = []
            for doc in nlp.pipe(sentences, disable=["tagger", "parser", "ner", "textcat"]): 
                lemmatized_sentences.append([token.lemma_ for token in doc])
            lemmatized_texts[key] = lemmatized_sentences 

        return lemmatized_text 

