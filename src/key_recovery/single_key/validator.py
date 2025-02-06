from .share import SingleKeyShare
from ..base.validator import Validator
from .generator import SingleKeyGenerator
from ..utils import to_hex_no_prefix, from_hex_no_prefix

class SingleKeyValidator(Validator):
    def __init__(self, commitment: str):
        super().__init__(commitment)

    # Validates the share
    # Returns True if share is valid
    #         False otherwise
    def validate_share(self, share: SingleKeyShare, password: str) -> bool:
        point = (from_hex_no_prefix(share.share[0]), from_hex_no_prefix(share.share[1]))
        generated_tag = SingleKeyGenerator.generate_tag(password, point, self._commitment)
        return share.tag == to_hex_no_prefix(generated_tag) and share.commitment == to_hex_no_prefix(self._commitment)
    
    # Validates generated secret
    # Returns True if secret is valid
    #         False otherwise
    def validate_secret(self, secret: int) -> bool:
        generated_commitment = SingleKeyGenerator.generate_commitment(secret)
        return self._commitment == generated_commitment

    # read only properties
    @property
    def commitment(self):
        return self._commitment