from math import ceil

def to_bytes(data) -> bytes:
    if isinstance(data, bytes):
        return data
    if isinstance(data, int):
        data = int(abs(data))
        data.to_bytes(ceil(data.bit_length() / 8), 'big')
    if isinstance(data, str):
        return data.encode()
    return str(data).encode()