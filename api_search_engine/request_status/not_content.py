class HttpNotContent(Exception):
    def __init__(self, code=204, message="Not Content"):
        self.code = code
        self.message = message

    def __str__(self):
        return repr(self.message)
