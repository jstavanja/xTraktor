def get_html_from_file(file_path, encoding=None):
    """
    Gets raw HTML from a saved .html file.

    Parameters
    ----------
    file_path : string
        Path to the file containing the HTML.

    Returns
    -------
    str
        HTML content fetched from the file in a string.
    """
    if encoding is not None:
        return open(file_path, 'r', encoding=encoding).read()
    else:
        return open(file_path, 'r').read()
