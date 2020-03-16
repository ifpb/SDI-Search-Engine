
class Service(object):
    def __init__(self, id, url, type, title, description, publisher, geometry):
        self.id = id
        self.url = url
        self.type = type
        self.title = title
        self.description = description
        self.publisher = publisher
        self.geometry = geometry

    def __str__(self):
        return self.__dict__

    def __repr__(self):
        return self
