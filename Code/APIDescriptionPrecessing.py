import xlrd
import xlsxwriter
import re

def filters(paragraph):
    d1 = filter_emoji(paragraph)  
    d2 = filter_url(d1)  
    d3 = filter_html_tag(d2)
    d4 = filter_char(d3)
    return d4

def filter_html_tag(paragraph):
    paragraph = paragraph.replace('<br>', ". ")
    paragraph = paragraph.replace('&amp;', "&")
    rule = "<[^>]*>"
    my_re = re.compile(rule, re.S)
    paragraph1 = my_re.sub(" ", paragraph)
    return paragraph1

def filter_url(paragraph):
    my_re = re.compile(r'[a-zA-z]+://[^\s]*', re.S)
    my_re_1 = re.compile(r'www+\.[^\s]*', re.S)
    my_re_2 = re.compile(r'[a-zA-Z0-9_-]+@+[a-zA-Z0-9_-]+\.com', re.S)
    paragraph1 = my_re.sub("", paragraph)
    paragraph2 = my_re_1.sub("", paragraph1)
    paragraph3 = my_re_2.sub("", paragraph2)
    return paragraph3

def filter_char(raw):
    raw = raw.replace('-', '_')
    # raw = raw.replace('’', "'")
    fil = re.compile(u'[^0-9a-zA-Z %.,_?!@"\'()+ ]', re.UNICODE)
    paragraph = fil.sub('. ', raw)
    paragraph = paragraph.replace('_', '-')
    my_re = re.compile("\((.*?)\)", re.S)
    paragraph = my_re.sub(" ", paragraph)
    return paragraph

def filter_emoji(paragraph):
    try:
        # Wide UCS-4 build
        myre = re.compile(u'['
                          u'\U0001F300-\U0001F64F'
                          u'\U0001F680-\U0001F6FF'
                          u'\u2600-\u2B55]+',
                          re.UNICODE)
    except re.error:
        # Narrow UCS-2 build
        myre = re.compile(u'('
                          u'\ud83c[\udf00-\udfff]|'
                          u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                          u'[\u2600-\u2B55])+',
                          re.UNICODE)
    return myre.sub('. ', paragraph)  # 替换字符串中的Emoji

def description_filter():
    workbook = xlrd.open_workbook("E:/APIDescription.xlsx")
    worksheet = workbook.sheet_by_index(0)
    nrows = worksheet.nrows
    workbook1 = xlsxwriter.Workbook('APIDescriptionFiltered.xlsx')
    worksheet1 = workbook1.add_worksheet()
    for i in range(nrows):
        worksheet1.write(i, 0, worksheet.cell_value(i, 0))
        worksheet1.write(i, 1, filters(worksheet.cell_value(i, 1)))
    workbook1.close()

if __name__ == '__main__':
    description_filter()