
from collections import defaultdict

import colibricore

class Coco:

    def __init__(self, tmpdir):
        self.tmpdir = tmpdir

    def set_lines(self, lines):
        self.lines = lines

    def simple_tokenize(self):
        for i, line in enumerate(self.lines):
            line = line.replace(',',' ,')
            line = line.replace('.',' .')
            line = line.replace(':',' :')
            self.lines[i] = line

    def set_file(self, ngramfile = False):
        if ngramfile:
            self.ngramfile = ngramfile
        else:
            self.ngram_file = self.tmpdir + 'ngrams.txt'
            with open(self.ngram_file, 'w', encoding = 'utf-8') as txt:
                for line in self.lines:
                    txt.write(line + '\n')            

    def model(self, min_tokens, max_ngrams):
        classfile = self.tmpdir + 'ngrams.colibri.cls'
        # Build class encoder
        self.classencoder = colibricore.ClassEncoder()
        self.classencoder.build(self.ngram_file)
        self.classencoder.save(classfile)

        # Encode corpus data
        corpusfile = tmpdir + 'ngrams.colibri.dat'
        self.classencoder.encodefile(self.ngram_file, corpusfile)

        # Load class decoder
        self.classdecoder = colibricore.ClassDecoder(classfile) 

        # Train model
        options = colibricore.PatternModelOptions(mintokens = min_tokens, maxlength = max_ngrams, doreverseindex=True)
        self.model = colibricore.IndexedPatternModel()
        self.model.train(corpusfile, options)

    def match(self, keys):
        key_matches = defaultdict(list)
        for key in keys:
            querypattern = self.classencoder.buildpattern(key)
            if querypattern in self.model:
                print(model[querypattern])
                print(dir(model[querypattern]))
                quit()
            else:
                key_matches[key] = [0,[]]
        return key_matches


