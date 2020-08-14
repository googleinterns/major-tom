import requests  # pylint: disable=import-error


def get_document(url, file_name):
    """Retrieves a PDF document from the specified URL
    Saves it as regs.pdf"""
    response = requests.get(url)
    open(file_name, 'wb').write(response.content)
