from ..base.recoverer import Recoverer
from .share import SingleKeyShare
from ..utils import from_hex_no_prefix


class SingleKeyRecoverer(Recoverer):
    def __init__(self, threshold: int, prime: int = None):
        super().__init__(threshold, prime)

    def recover(self, shares: list[SingleKeyShare]) -> int:
        points = []
        unique_x = set()
        for share in shares:
            x = from_hex_no_prefix(share.share[0])
            y = from_hex_no_prefix(share.share[1])
            if x in unique_x:
                continue
            unique_x.add(x)
            points.append((x, y))
        if len(points) < self.threashold:
            raise ValueError("Not enough shares to recover the key")
        
        return self._lagrange_interpolation(points)
    
    def _lagrange_interpolation(self, points: list[tuple[int, int]]) -> int:
        result = 0
        for i in range(len(points)):
            xi, yi = points[i]
            term = yi
            for j in range(len(points)):
                if i == j:
                    continue
                xj, yj = points[j]
                if self.prime is not None:
                    term *= xj * pow(xj - xi, -1, self.prime)
                else:
                    term *= xj / (xj - xi)
            result += term
            if self.prime is not None:
                result %= self.prime
        return int(result)