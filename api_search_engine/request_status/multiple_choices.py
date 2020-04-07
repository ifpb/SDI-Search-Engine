class HttpMultipleChoices(Exception):
    def __init__(self, code=300, message="Multiple choices"):
        self.code = code
        self.message = message

    def __str__(self):
        return repr(self.message)
