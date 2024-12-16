import tomotopy as tp
import numpy as np
import pyLDAvis


class Visualize: 


    @staticmethod 
    def visualization(): 
        # Load corpus 
        corpus = tp.utils.Corpus.load('models/corpus.cps')

        #Load model 
        mdl = tp.LDAModel.load('models/lda_model.bin')   

        # Print summary 
        print('Num docs:{}, Num Vocabs:{}, Total Words:{}'.format(
            len(mdl.docs), len(mdl.used_vocabs), mdl.num_words
        ))
        print('Removed Top words: ', *mdl.removed_top_words)

        # Store variables 
        topic_term_dists = np.stack([mdl.get_topic_word_dist(k) for k in range(mdl.k)])
        doc_topic_dists = np.stack([doc.get_topic_dist() for doc in mdl.docs])
        doc_topic_dists /= doc_topic_dists.sum(axis=1, keepdims=True)
        doc_lengths = np.array([len(doc.words) for doc in mdl.docs])
        vocab = list(mdl.used_vocabs)
        term_frequency = mdl.used_vocab_freq

        # Prepare for visualization 
        prepared_data = pyLDAvis.prepare(
            topic_term_dists, 
            doc_topic_dists, 
            doc_lengths, 
            vocab, 
            term_frequency,
            start_index=0, # tomotopy starts topic ids with 0, pyLDAvis with 1
            sort_topics=False # IMPORTANT: otherwise the topic_ids between pyLDAvis and tomotopy are not matching!
        )
        
        # Visualize 
        pyLDAvis.save_html(prepared_data, 'models/ldavis.html')
        # pyLDAvis.show(prepared_data, local=False)
 
# Call the function         
Visualize.visualization()