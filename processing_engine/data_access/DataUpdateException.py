class DataUpdateException(Exception):
    def __init__(self, message='Falha ao atulizar dados no banco'):
        self.message = message

    def __str__(self):
        return repr(self.message)