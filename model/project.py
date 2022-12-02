from sys import maxsize
import random
import string

def random_string(prefix, max_length):
    symbols = string.ascii_letters + string.digits + string.punctuation + " "*10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(max_length))])

class Project:
    def __init__(self, name=None, description=None, id=None):
        self.name = name
        self.description = description
        self.id = id

    def __repr__(self):
        return f"{self.id}:{self.name}:{self.description}"

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize