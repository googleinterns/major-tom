import requests


def get_document(url):
    """Retrieves a PDF document from the specified URL
    Saves it as regs.pdf"""
    response = requests.get(url)
    open('regs.pdf', 'wb').write(response.content)
