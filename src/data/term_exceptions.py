__author__ = 'aparaatti'


class TermAlreadyExists(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class DescriptionAlreadySetException(Exception):
    def __init__(self, value):
        """

        :param term:
        """
        self.value = \
            "Term: " + value + " already has a Description object."\
            + " Edit current description through provided methods."

    def __str__(self):
        return repr(self.value)


class LinksAlreadySetException(Exception):
    def __init__(self, value):
        self.value = \
            "Term: " + value + " already has a Links object."\
            + " Edit current links through provided methods."

    def __str__(self):
        return repr(self.value)