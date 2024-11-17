class NoClientError(Exception):
    def __init__(self):
        super().__init__("No Client")


class NotAuthorizedAccountError(Exception):
    def __init__(self):
        super().__init__("User not authorized")
