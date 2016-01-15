
import sys
import os

import featurizer
import vectorizer
import utils
import docreader

infile = sys.argv[1]
outfile = sys.argv[2]
textindex = int(sys.argv[3])

dr = docreader.Docreader()
dr.parse_doc(infile)

raws = [line[textindex] for line in dr.lines]
tagged = utils.tokenized_2_tagged(raws)
feature_config = { 'token_ngrams' : {'n_list' : [1]} }

ft = featurizer.Featurizer(raws, tagged, os.getcwd(), feature_config)
ft.fit_transform()
instances, vocabulary = ft.return_instances(['token_ngrams'])

vr = vectorizer.Vectorizer(instances, instances, ['x' for x in range(len(dr.lines))], prune = 10000)
vr.weight_features()
vr.prune_features()
train, test, top_features, feature_weights = vr.vectorize()

top_features_vocab = [vocabulary[i] for i in top_features]
feature_weights = zip(top_features_vocab, feature_weights)
with open(outfile, 'w', encoding = 'utf-8') as counts_out:
    for fw in feature_weights:
        counts_out.write(' '.join([str(x) for x in fw]) + '\n')
