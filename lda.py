import os
import sys
import json
import pandas as pd
import numpy as np
import tomotopy as tp

class LDA:
    
    def __init__(self, input_data, num_topics=20, save_path=None): 
        """
        Initialize the LDA class.

        Args:
            input_data (dict): Preprocessed input data as a dictionary.
            num_topics (int): Number of topics for the LDA model. Defaults to 20.
            save_path (str): Path to save the trained LDA model. Defaults to None.
        """
        self.input_data = input_data
        self.num_topics = num_topics
        self.save_path = save_path

    def split_data(self, train_ratio=0.8): 
        """
        Split input data into training and test sets.

        Args:
            train_ratio (float): Proportion of data to use for training. Defaults to 0.8.

        Returns:
            tuple: Training and test corpora (as `tomotopy.utils.Corpus` objects).
        """
        if not self.input_data or not isinstance(self.input_data, dict):
            raise ValueError("Input data must be a non-empty dictionary.")

        n = len(self.input_data)
        train_n = round(n * train_ratio)

        train_pairs = {k: self.input_data[k] for k in list(self.input_data)[:train_n]}
        test_pairs = {k: self.input_data[k] for k in list(self.input_data)[train_n:]}

        train_data = [item for sublist in train_pairs.values() for item in sublist if len(item) > 1]
        test_data = [item for sublist in test_pairs.values() for item in sublist if len(item) > 1]

        train_corpus = tp.utils.Corpus(tokenizer=tp.utils.SimpleTokenizer())
        test_corpus = tp.utils.Corpus(tokenizer=tp.utils.SimpleTokenizer())
        train_corpus.process(train_data)
        test_corpus.process(test_data)

        return train_corpus, test_corpus

    def train_lda(self, train_corpus, min_cf=3, rm_top=5, burn_in=100, num_iterations=10000):
        """
        Train the LDA model.

        Args:
            train_corpus (tomotopy.utils.Corpus): Training corpus.
            min_cf (int): Minimum collection frequency for words. Defaults to 3.
            rm_top (int): Number of most frequent words to remove. Defaults to 5.
            burn_in (int): Number of burn-in iterations. Defaults to 100.
            num_iterations (int): Number of iterations for training. Defaults to 10000.

        Returns:
            tp.LDAModel: Trained LDA model.
        """
        if not train_corpus or not len(train_corpus):
            raise ValueError("Training corpus is empty or invalid.")

        mdl = tp.LDAModel(
            tw=tp.TermWeight.ONE, 
            min_cf=min_cf, 
            rm_top=rm_top, 
            k=self.num_topics, 
            corpus=train_corpus
        )

        mdl.burn_in = burn_in
        mdl.train(0)
        print(f"Vocabulary Size: {len(mdl.used_vocabs)}, Total Words: {mdl.num_words}")
        print(f"Removed Top Words: {mdl.removed_top_words}")
        mdl.train(num_iterations, show_progress=True)

        if self.save_path:
            mdl.save(self.save_path, True)
            print(f"Model saved to {self.save_path}")

        return mdl

    def summarize_topics(self, model, top_n=10):
        """
        Summarize topics from the trained LDA model.

        Args:
            model (tp.LDAModel): Trained LDA model.
            top_n (int): Number of words to display per topic. Defaults to 10.

        Returns:
            list: List of topics with their top words.
        """
        topics = []
        for k in range(model.k):
            topic_words = model.get_topic_words(k, top_n=top_n)
            topics.append({"Topic": k, "Words": topic_words})
            print(f"Topic #{k}:")
            for word, prob in topic_words:
                print(f"\t{word}: {prob:.4f}")
        return topics

    def document_topics(self, model):
        """
        Extract dominant topics for each document in the corpus.

        Args:
            model (tp.LDAModel): Trained LDA model.

        Returns:
            list: List of documents with their dominant topic and words.
        """
        doc_topics = []
        for i, doc in enumerate(model.docs):
            topic_dist = doc.get_topic_dist()
            dominant_topic = topic_dist.argmax()
            topic_words = model.get_topic_words(dominant_topic)
            doc_topics.append({
                "Document": i,
                "Dominant Topic": dominant_topic,
                "Words": topic_words
            })
            print(f"Document {i}: Dominant Topic #{dominant_topic}, Words: {topic_words}")
        return doc_topics
