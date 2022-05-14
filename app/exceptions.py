class HeavyMetalException(Exception):
    """The base class for all custom exceptions defined for this application."""
    pass


class AuthenticationError(HeavyMetalException):
    """Indicates that a username or password was provided that was invalid."""
    pass
