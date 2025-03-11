import tomotopy as tp 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors 
import re 
import json 

corpus = tp.utils.Corpus()
dictionary = json.load(open("preprocessing/preprocessing.json"))
for key, value in dictionary.items():
    for index, key in enumerate(value): 
        corpus.add_doc(value, numeric_metadata=[float(index)], metadata=value)    
mdl = tp.GDMRModel(tw=tp.TermWeight.ONE, k=30, degrees=[6], 
    alpha=1e-2, sigma=0.25, sigma0=3.0, decay=1.0,
    metadata_range=[(2000, 2017)], corpus=corpus
)
mdl.optim_interval = 20
mdl.burn_in = 200

mdl.train(1000)

print('Num docs:{}, Num Vocabs:{}, Total Words:{}'.format(
    len(mdl.docs), len(mdl.used_vocabs), mdl.num_words
))

# Let's train the model
mdl.train(1000, show_progress=True)
mdl.summary()

# Let's visualize the result
topic_counts = mdl.get_count_by_topics()
lambdas = mdl.lambdas
lambdas = lambdas.reshape(lambdas.shape[:1] + (len(mdl.metadata_dict), -1))
# lambdas shape: [num_topics, num_categorical_metadata, degrees + 1]

md_range = mdl.metadata_range
r = np.stack([mdl.tdf_linspace(
    [md_range[0][0]], 
    [md_range[0][1]], 
    [50], # interpolation size
    cat
) for cat in mdl.metadata_dict])
# r shape: [num_categorical_metadata, 50, num_topics]

xs = np.linspace(*md_range[0], 50)
for k in (-topic_counts).argsort():
    print('Topic #{} ({})'.format(k, topic_counts[k]))
    print(*(w for w, _ in mdl.get_topic_words(k)))
    print('Lambda:', lambdas[k].reshape((len(mdl.metadata_dict), -1)))

    for label, ys in zip(mdl.metadata_dict, r[:, :, k]):
        label = re.sub(r'^(Proceedings|Journal)( of)?( the)?( -)?|International Conference on', '', label).strip()
        if len(label) >= 35: label = label[:33] + '...'
        plt.plot(xs, ys, linewidth=2, label=label)
    plt.title('#{}\n({})'.format(k, ' '.join(w for w, _ in mdl.get_topic_words(k, top_n=5))))
    plt.legend()