class User:
    def __init__(self, id, name, channel):
        self.id = id
        self.name = name
        self.channel = channel

    def __eq__(self, other):
        return self.id == other.id
