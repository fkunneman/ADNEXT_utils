
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
            line = line.replace(';',' ;')
            line = line.replace('!',' !')
            line = line.replace('?',' ?')
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

    def model_ngramperline(self, ngrams, write = False):
        # Write txt file
        ngramperline_file = self.tmpdir + 'ngramperline.txt'
        with open(ngramperline_file, 'w', encoding = 'utf-8') as ngw:
            ngw.write('\n'.join(ngrams) + '\n')
        # Build class encoder
        classfile = self.tmpdir + 'ngrams.colibri.cls'
        self.classencoder = colibricore.ClassEncoder()
        self.classencoder.processcorpus(ngramperline_file)
        self.classencoder.processcorpus(self.ngram_file)
        self.classencoder.buildclasses()
        self.classencoder.save(classfile)

        # Encode corpus data
        corpusfile_ngram = self.tmpdir + 'ngramperline.colibri.dat'
        self.classencoder.encodefile(ngramperline_file, corpusfile_ngram)

        corpusfile_test = self.tmpdir + 'ngrams.colibri.dat'
        self.classencoder.encodefile(self.ngram_file, corpusfile_test)

        # Load class decoder
        self.classdecoder = colibricore.ClassDecoder(classfile) 

        # Train model
        options = colibricore.PatternModelOptions(mintokens = 1, dopatternperline = True, maxlength = 10)
        refmodel = colibricore.IndexedPatternModel()
        refmodel.train(corpusfile_ngram, options)

        # Test model
        options = colibricore.PatternModelOptions(mintokens = 1, maxlength = 10)
        self.model = colibricore.IndexedPatternModel()
        self.model.train(corpusfile_test, options, refmodel)
        if write:
            print('writing to file')
            self.model.write(self.tmpdir + 'ngrams.IndexedPatternModel_constrained')

    def model(self, min_tokens, max_ngrams, classfile = False, corpusfile = False, write = False):
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
        self.model.train(corpusfile, options)
        if write:
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
                key_matches[key] = matches
        return key_matches
