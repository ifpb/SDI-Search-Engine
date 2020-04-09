class MultipleChoices(Exception):
    def __init__(self, code=300, message="Multiple choices", data=None):
        self.code = code
        self.message = message
        self.data = data

    def __str__(self):
        return repr(self.message)
