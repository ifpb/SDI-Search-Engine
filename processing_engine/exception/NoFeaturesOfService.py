class NoFeaturesOfService(Exception):
    def __init__(self, message='Service without features or already exists'):
        self.message = message

    def __str__(self):
        return repr(self.message)