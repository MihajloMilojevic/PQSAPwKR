from .share import Share

class Validator:
    def __init__(self, commitment: str):
        self._commitment = commitment

    # Validates the share
    # Returns True if share is valid
    #         False otherwise
    def validate_share(self, share: Share, password: str) -> bool:
        raise NotImplementedError
    
    # Validates generated secret
    # Returns True if secret is valid
    #         False otherwise
    def validate_secret(self, secret: int) -> bool:
        raise NotImplementedError


    # read only properties
    @property
    def commitment(self):
        return self._commitment