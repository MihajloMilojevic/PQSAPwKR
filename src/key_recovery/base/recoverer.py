
from .share import Share

class Recoverer:
    def __init__(self, threashold: int, prime: int = None):
        self._threashold = threashold
        self._prime = prime

    def recover(self, shares: list[Share]) -> int:
        raise NotImplementedError
    
    # read only properties

    @property
    def threashold(self) -> int:
        return self._threashold
    
    @property
    def prime(self) -> int:
        return self._prime