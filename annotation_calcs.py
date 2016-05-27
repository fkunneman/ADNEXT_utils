#!/usr/bin/env python

import matplotlib.pyplot as plt
from collections import defaultdict
import itertools
import numpy

from pynlpl import evaluation


class Annotation_calculator:

    def __init__(self, lines):
        self.lines = lines
        self.num_annotators = len(lines[0])
        self.num_items = len(self.lines)
        self.annotations = list(set(list(itertools.chain(*self.lines))))
        self.annotator_perms = list(itertools.permutations(range(self.num_annotators), 2))
        self.annotation_combs = list(itertools.combinations(self.annotations, 2))

    def performance(self):
        majority = int(round(self.num_annotators / 2))
        majorities = range(majority, self.num_annotators + 1)
        percentage_performance = []
        for m in majorities:
            performance = [1 if l.count(1) >= m else 0 for l in self.lines]
            percentage = str(int((m / self.num_annotators) * 100)) + '% positive'
            percentage_performance.append([percentage, performance])
        return percentage_performance    

    def calculate_precision(self):
        pp = self.performance()
        precision = []
        for percentage in pp:
            precision.append([percentage[0], round(percentage[1].count(1) / self.num_items, 2)])
        return precision    

    def calculate_fscore(self, index_1, index_2):
        ce = evaluation.ClassEvaluation()
        for item in self.lines:
            ce.append(item[index_1], item[index_2])
        return round(ce.fscore(cls = 1), 2)

    def calculate_mutual_fscore(self):
        fscores = []
        perms = list(itertools.permutations(range(self.num_annotators), 2))
        for p in perms:
            fscores.append(self.calculate_fscore(p[0],p[1]))
        mutual_fscore = round(sum(fscores) / len(fscores), 2)
        return mutual_fscore

    def calculate_cohens_kappa(self):    
        cohens_kappas = []
        for annotator_perm in self.annotator_perms:
            match = sum([1 for l in self.lines if l[annotator_perm[0]] == l[annotator_perm[1]]])
            odd = self.num_items - match
            agreement = match / self.num_items
            random = 0        
            for annotation in self.annotations:
                percent_annotator_1 = sum([1 for l in self.lines if l[annotator_perm[0]] == annotation]) / self.num_items
                percent_annotator_2 = sum([1 for l in self.lines if l[annotator_perm[1]] == annotation]) / self.num_items
                random += (percent_annotator_1 * percent_annotator_2)
            ck = (agreement - random) / (1 - random)
        cohens_kappas.append(ck)    
        cohens_kappa = round(numpy.mean(cohens_kappas), 2)
        return cohens_kappa

    def calculate_krippendorffs_alpha(self):
        item_agreement = 0
        agreement = 0
        for annotation_perm in self.annotation_combs:
            item_agreement += sum([l.count(annotation_perm[0]) * l.count(annotation_perm[1]) for l in self.lines])
            agreement += (sum([l.count(annotation_perm[0]) for l in self.lines]) * sum([l.count(annotation_perm[1]) for l in self.lines]))
        multiplier_oa = 1 / (self.num_items * self.num_annotators * (self.num_annotators - 1))
        DO = item_agreement * multiplier_oa
        multiplier_ea = 1 / (self.num_items * self.num_annotators * ((self.num_items * self.num_annotators) - 1))
        DE = agreement * multiplier_ea
        KA = round(1 - (DO / DE), 2)
        return KA     

    def output_annotation_scores(self, outfile):
        output = self.calculate_precision()
        output.append(['Cohens Kappa', self.calculate_cohens_kappa()])
        output.append(['Krippendorffs_alpha', self.calculate_krippendorffs_alpha()])
        output.append(['Mutual fscore', self.calculate_mutual_fscore()]) 
        with open(outfile, 'w') as scores_out:
            scores_out.write('\n' + '\n'.join(['\t'.join([str(y) for y in x]) for x in output]))

    def plot_precision_at(self, outfile):
        pp = self.performance()
        legend_entries = [p[0] for p in pp]
        ranks = range(1, self.num_items + 1)
        for percentage in pp:
            precisions = [(percentage[1][:i + 1].count(1) / (i + 1)) for i in ranks]
            plt.plot(ranks, precisions)
        plt.ylim((0,1))
        plt.legend(legend_entries, loc = 'lower right')
        plt.ylabel('precision at rank', fontsize = 16)
        plt.xlabel('rank', fontsize = 16)
        plt.tick_params(axis = 'both', which = 'major', labelsize = 16)
        plt.tick_params(axis = 'both', which = 'minor', labelsize = 16)
        plt.savefig(outfile)
