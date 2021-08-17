class DirectoryNotFoundError(FileNotFoundError):
    pass

class AmbiguousSelectionException(Exception):
    pass

class NoSelectionException(Exception):
    pass