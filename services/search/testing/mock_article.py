class Article:
    """
    Has all the attributes that an article table will have in the db
    Attributes:
        id: given id in db
        number: article number extracted from the pdf
        content: article's full text
        keywords: frequency map of the keywords from the content
    """
    def __init__(self, id, number, content, keywords):
        self.id = id
        self.number = number
        self.content = content
        self.keywords = keywords
