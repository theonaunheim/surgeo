class SurgeoError(Exception):
    '''Custom error class for vanity's sake.'''

    def __init__(self, reason, response=None):
        self.reason = reason
        self.response = response
        Exception.__init__(self, reason)

    def __str__(self):
        return self.reason
