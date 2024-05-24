class CustomHttpException(Exception):
    """
    A custom exception class for handling HTTP exceptions.

    Attributes
    ----------
    status_code : int
        an integer that represents the HTTP status code
    content : int | dict
        an integer or dictionary that represents the content of the HTTP response

    Methods
    -------
    __init__(self, status_code: int, content: int | dict = None):
        Initializes the CustomHttpException with the given status code and content.
    """
    def __init__(self, status_code: int, content: int | dict = None):
        self.status_code = status_code
        self.content = content


