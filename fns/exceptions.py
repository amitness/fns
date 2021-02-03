class ValidationError(Exception):
    """
    A class for validation errors.

    """

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __unicode__(self):
        return self.message

    def __str__(self):
        return self.message.encode("utf-8")
