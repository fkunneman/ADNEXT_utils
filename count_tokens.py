
import sys

import docreader
from framework import calculations

infile = sys.argv[1]
outfile = sys.argv[2]
textindex = int(sys.argv[3])

dr = docreader.Docreader()
dr.parse_doc(infile)

feature_weights = calculations.count_tokens(dr.lines)

with open(outfile, 'w', encoding = 'utf-8') as counts_out:
    for fw in feature_weights:
        counts_out.write(' '.join([str(x) for x in fw]) + '\n')
