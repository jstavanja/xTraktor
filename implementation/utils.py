def get_html_from_file(file_path, encoding=None):
    """
    Gets raw HTML from a saved .html file.

    Parameters
    ----------
    file_path: str
        Path to the file containing the HTML

    encoding: str, optional
        Encoding to use for reading an HTML file. Common options are
        'utf8', 'cp1250', 'iso 8859-1'. If not specified, UTF-8 will
        be used

    Returns
    -------
    str
        HTML content fetched from the file in a string
    """
    if encoding is not None:
        return open(file_path, 'r', encoding=encoding).read()
    else:
        return open(file_path, 'r').read()
