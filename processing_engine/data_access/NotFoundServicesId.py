class NotFoundServicesId(Exception):
    def __init__(self, message='Nenhum id de serviço foi encontrado'):
        self.message = message

    def __str__(self):
        return repr(self.message)
