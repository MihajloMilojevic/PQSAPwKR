from dataclasses import dataclass
from ..base.share import Share

@dataclass
class SingleKeyShare(Share):
    share: tuple[str, str]
    tag: str
    commitment: str
