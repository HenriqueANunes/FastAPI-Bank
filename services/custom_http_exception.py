class CustomHttpException(Exception):
    def __init__(self, status_code: int, content: str | dict = None):
        self.status_code = status_code
        self.content = content


