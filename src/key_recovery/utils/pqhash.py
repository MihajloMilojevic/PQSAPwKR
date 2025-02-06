import hashlib
from .to_bytes import to_bytes


def pqhash(*data) -> bytes:
    return hashlib.sha3_256(b"".join([to_bytes(x) for x in data])).digest()[:32]
