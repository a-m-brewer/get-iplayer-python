class BbcException(Exception):
    pass


class UserInputException(BbcException):
    pass


class ArgumentException(BbcException):
    pass


class MissingDataException(BbcException):
    pass
