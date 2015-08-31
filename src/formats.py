# There comes a time in one's life when excel files must be parsed.

import xlrd

def sheets_from_excel(xlspath):
    """
    Reads in an xls(x) file,
    returns an array of arrays, like:
    Xijk, i = sheet, j = row, k = column
    (but it's not a np ndarray, just nested arrays)
    """
    wb = xlrd.open_workbook(xlspath)
    n_sheets = wb.nsheets
    sheet_data = []
    for sn in xrange(n_sheets):
        sheet = wb.sheet_by_index(sn)
        rows = [sheet.row_values(i) for i in xrange(sheet.nrows)]
        if len(rows) > 0:
            sheet_data.append(rows)
    return sheet_data
