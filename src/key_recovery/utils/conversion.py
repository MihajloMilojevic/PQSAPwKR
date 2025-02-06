
def to_hex_no_prefix(data: int) -> str:
    return hex(data)[2:]

def from_hex_no_prefix(data: str) -> int:
    return int("0x" + data, 16)