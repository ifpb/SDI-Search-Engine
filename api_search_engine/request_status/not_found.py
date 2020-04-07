class HttpNotFound(Exception):
    def __init__(self, code=404, message="Not Found"):
        self.code = code
        self.message = message

    def __str__(self):
        return repr(self.message)
