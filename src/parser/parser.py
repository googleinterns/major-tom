from PyPDF2 import PdfFileReader
from pprint import pprint

def text_extractor():
    pass

def remove_extra_spaces():
    pass

def remove_footer():
    pass

def separate_into_articles():
    pass

def text_extractor(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)

        last = None

        for page in pdf.pages:
            last = page.extractText()

            print(last)

            # Remove '/n' from all string elements.
            page = last.replace(' \n', '')
            page = page.translate({ord('\n'): None})

            # Remove extra spaces
            # page = page.replace('  ', ' ')
            # page = page.translate({ord(i): ' ' for i in '  '})

            last = page
            # pprint(last)
            # print(last)
            
            # pprint(page.extractText())
            # print(type(page))
            # print(type(page.extractText()))
        # print(type(pdf))





def get_info(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
        n_pages = pdf.getNumPages()
    print(info)
    print(n_pages)


if __name__ == '__main__':
    path = 'regs.pdf'
    text_extractor(path)
