
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

    def set_file(self):
        self.ngram_file = self.tmpdir + 'ngrams.txt'
        with open(self.ngram_file, 'w', encoding = 'utf-8') as txt:
            for line in self.lines:
                txt.write(line + '\n')

    def load_file(self, filename):
        self.ngram_file = filename
    
    def load_classencoder(self, classencoder):
        self.classencoder = colibricore.ClassEncoder(classencoder)

    def load_classdecoder(self, classfile):
        self.classdecoder = colibricore.ClassDecoder(classfile)

    def load_model(self, modelfile):
        self.model = colibricore.IndexedPatternModel(modelfile)

    def model(self, min_tokens, max_ngrams, classfile = False, corpusfile = False):
        # Build class encoder
        if classfile:
            self.classencoder = colibricore.ClassEncoder(classfile)
        else:
            classfile = self.tmpdir + 'ngrams.colibri.cls'
            self.classencoder = colibricore.ClassEncoder()
            self.classencoder.build(self.ngram_file)
            self.classencoder.save(classfile)

        # Encode corpus data
        if not corpusfile:
            corpusfile = self.tmpdir + 'ngrams.colibri.dat'
            self.classencoder.encodefile(self.ngram_file, corpusfile)

        # Load class decoder
        self.classdecoder = colibricore.ClassDecoder(classfile) 

        # Train model
        options = colibricore.PatternModelOptions(mintokens = min_tokens, maxlength = max_ngrams, doreverseindex = True)
        self.model = colibricore.IndexedPatternModel()
        self.model.train(corpusfile, options)
        #print(dir(self.model))
        #self.model.printmodel()
        print('writing to file')
        self.model.write(self.tmpdir + 'ngrams.IndexedPatternModel')

    def match(self, keys):
        key_matches = defaultdict(list)
        for key in keys:
            querypattern = self.classencoder.buildpattern(key)
            if querypattern in self.model:
                match = self.model.getdata(querypattern)
                matches = []
                for x in match:
                    matches.append(x[0] - 1)
                count = len(match)
                key_matches[key] = [count, matches]
            else:
                key_matches[key] = [0,[]]
        return key_matches
