
import xlwt
import re

import gen_functions

class Linewriter:

    def __init__(self, lines):
        self.lines = lines

    def write_xls(self, headers, header_style, outfile):
        if len(self.lines) > 65535:
            num_chunks = int(len(self.lines) / 65534) + 1
            chunks = gen_functions.make_chunks(self.lines, nc = num_chunks)
        else:
            chunks = [self.lines]
        book = xlwt.Workbook(encoding = 'utf-8')
        #algn1 = xlwt.Alignment()
        #algn1.wrap = 1
        style = xlwt.XFStyle()
        #style.alignment = algn1
        for sheetno, chunk in enumerate(chunks):
            tabname = 'sheet_' + str(sheetno)
            tab = book.add_sheet(tabname)
            for i, header in enumerate(headers):
                tab.write(0, i, header, style)
            for i, line in enumerate(chunk):
                i += 1
                for j, column in enumerate(line):
                    if re.search('^http', str(column)):
                        url = 'HYPERLINK(\"' + column + '\"; \"' + column + '\")'
                        tab.write(i, j, xlwt.Formula(url))
                    else:
#                        style = xlwt.XFStyle()
#                        style.alignment = algn1
                        style.num_format_str = header_style[headers[j]]
                        try:
                            column.encode('utf-8')
                            tab.write(i, j, column, style)
                        except:
                            print('corrupt text, skipping')
                            continue
        book.save(outfile)

    def write_txt(self, outfile, delimiter = '\t'):
        with open(outfile, 'w', encoding = 'utf-8') as out:
            for line in self.lines:
                out.write(delimiter.join([str(x) for x in line]) + '\n')
