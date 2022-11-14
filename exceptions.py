from utils import status


class MyBasicException(Exception):

    def __init__(self, message, status, description=None):
        self.message = message
        self.description = description
        self.status = status

    def __str__(self):
        if self.description:
            return f"{self.message}\n{self.description}"

        return self.message

# Normal Error

class BadRequestError(MyBasicException):

    def __init__(self, message="BAD_REQUEST", description=None, status=status.HTTP_400_BAD_REQUEST):
        super().__init__(message, description=description, status=status)


class ForbiddenError(MyBasicException):

    def __init__(self, message="FORBIDDEN", description=None):
        super().__init__(message, description=description, status=status.HTTP_403_FORBIDDEN)


class NotFoundError(MyBasicException):

    def __init__(self, message="NOT_FOUND", description=None):
        super().__init__(message, description=description, status=status.HTTP_404_NOT_FOUND)


class MethodNotAllowedError(MyBasicException):

    def __init__(self, message="METHOD_NOT_ALLOWED", description=None):
        super().__init__(message, description=description, status=status.HTTP_405_METHOD_NOT_ALLOWED)
