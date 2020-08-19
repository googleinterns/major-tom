import parser


class Article:
    """Class for storing articles.
    """
    def __init__(self, number, text):
        self.number = number
        self.text = text

    def to_dict(self):
        article_dict = {
            "articleNumber": self.number,
            "text": self.text,
            "wordCount": len(self.text.split())
        }
        return article_dict


mty_document = {
        "hash":
        "afafbfbdce8c40924edae00f6ce54f0c639ce42a2" +
        "c0fbbfa6ab82ea6925827c51",
        "jurisdiction":
        "Monterrey",
        "url":
        "http://www.guadalupe.gob.mx/wp-content/up" +
        "loads/2019/09/Nuevo-Reglamento-Homologado-1.pdf",
    }

mock_article_values = [
                        Article(1, "Este es un ariculo del reglamento de transito"),
                        Article(2, "Este es otro articulo del reglamento de transito"),
                        Article(3, "Este es el ultimo articulo del reglamento de transito.")
                        ]
