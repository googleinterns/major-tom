import slate


import logging

# import numpy

logging.basicConfig(level=logging.INFO)


class Article:
    def __init__(self, number, text):
        self.number = number
        self.text = text


def count_articles(pdf_text):
    articles = []
    article_text = ""
    article_count = 1
    i = 0
    while i < len(pdf_text) - 1:
        if (pdf_text[i] == "artículo" or pdf_text[i] == "articulo") and (
            pdf_text[i + 1] == str(article_count) + ".-"
            or pdf_text[i + 1] == str(article_count) + "-"
            or pdf_text[i + 1] == str(article_count) + "."
        ):
            logging.info("Article #" + str(article_count) + " recognized!")
            articles.append(Article(article_count, article_text))
            article_text = ""
            article_count += 1
            i += 1
        else:
            article_text += " " + pdf_text[i]
        i += 1
    for article in articles:
        logging.info("Article: " + str(article.number - 1) + " Text: " + article.text)


with open("regs.pdf", "rb") as f:
    doc = slate.PDF(f)

    final_text = ""
    for page in doc:
        why = page
        final_text += page
    final_text = final_text.strip().lower().split()
    # final_text_pass = final_text
    # final_text = numpy.array(final_text)
    # numpy.savetxt("foo.txt", final_text, fmt="%s")
    # print(final_text)
    count_articles(final_text)
