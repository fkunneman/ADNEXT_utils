
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
                            print(j, column, headers[j], style.num_format_str)
                            tab.write(i, j, column, style)
                        except:
                            continue
        book.save(outfile)
