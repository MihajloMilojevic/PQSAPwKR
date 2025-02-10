from .share import Share

class Generator:
    def __init__(self, threshold: int, prime: int = None):
        self._threshold = threshold
        self._prime = prime
        self._commitment = None
        self._secret = None
    
    # creates a commitment to the secret
    def commit(secret: int) -> str:
        raise NotImplementedError

    def generate_shares(self, password: str, n: int, start: int = 1, 
                        kdf_time_cost = 3, kdf_memory_cost = 2**16,
                        kdf_parallelism = 1) -> list[Share]:
        raise NotImplementedError

    # read only properties
    @property
    def threshold(self):
        return self._threshold

    @property
    def prime(self):
        return self._prime

    @property
    def commitment(self):
        return self._commitment