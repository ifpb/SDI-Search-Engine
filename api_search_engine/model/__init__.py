class Place:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return self.__dict__

