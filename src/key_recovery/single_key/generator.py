from ..base.generator import Generator
from ..utils import pqhash, to_bytes, to_hex_no_prefix
from .share import SingleKeyShare
import random
from argon2.low_level import hash_secret_raw, Type


class SingleKeyGenerator(Generator):
    def __init__(self, threashold: int, prime: int = None):
        super().__init__(threashold, prime)

    def commit(self, secret):
        self._secret = secret
        self._commitment = SingleKeyGenerator.generate_commitment(secret)
        return self._commitment
    
    def generate_shares(self, password: str, n: int, start: int = 1, 
                        kdf_time_cost = 3, kdf_memory_cost = 2**16,
                        kdf_parallelism = 1) -> list[SingleKeyShare]:
        # we have the threashold t
        # so polynomial will be of degree t-1
        # coeficients c1, c2, ..., ct-1 will be random
        # and coeficinet c0 will be the secret
        # so polynomial will be represented as a list of length t
        polynomial = [0] * self.threshold
        for i in range(1, self.threshold):
            if self._prime is not None:
                polynomial[i] = random.randint(1, self.prime - 1)
            else:
                polynomial[i] = random.randint(1, 2**32 - 1)
        polynomial[0] = self._secret

        shares = []
        for i in range(start, start + n):
            # generate share for i
            share = SingleKeyGenerator.generate_share(polynomial, i, self._prime)
            
            # generate the verification tag
            tag = SingleKeyGenerator.generate_tag(password, (i, share), self._commitment, kdf_time_cost, kdf_memory_cost, kdf_parallelism)
            
            # share object will hold hex representation of share, tag and commitment 
            # without "0x" prefix
            share_object = SingleKeyShare(
                (to_hex_no_prefix(i), to_hex_no_prefix(share)),     # share as point (i, polynomial(i))
                to_hex_no_prefix(tag),                              # tag
                to_hex_no_prefix(self._commitment)                  # commitment
            )

            shares.append(share_object)

        return shares

    @staticmethod
    def generate_commitment(secret: int) -> int:
        secret_hash = pqhash()
        xor = secret ^ int.from_bytes(secret_hash, 'big')
        commit_hash = pqhash(xor)
        return int.from_bytes(commit_hash, 'big')

    @staticmethod
    def generate_share(polynomial, x, prime):
        share = 0
        i = 1   # x^0
        for j in range(len(polynomial)):
            share += polynomial[j] * i
            i *= x  # x^j
            if prime is not None:
                i %= prime
                share %= prime
        return share


    @staticmethod
    def generate_tag(password: str, share: tuple[int, int], commitment: int, kdf_time_cost = 3, kdf_memory_cost = 2**16, kdf_parallelism = 1):
        # P + C(S) in the docs
        password_bytes = password.encode() + to_bytes(share[0]) + to_bytes(share[1])

        # Use Argon2 to derive a secure key from the password and commitment as salt
        derived_key = hash_secret_raw(
            secret=password_bytes,
            salt=to_bytes(commitment),              # Commitment is used as the salt
            time_cost=kdf_time_cost,                # Computational cost
            memory_cost=kdf_memory_cost,            # Memory usage (64MB)
            parallelism=kdf_parallelism,            # Number of parallel threads
            hash_len=32,                            # Output key size
            type=Type.ID                            # Recommended Argon2 variant
        )

        tag_hash = pqhash(commitment, share, derived_key)
        tag_int = int.from_bytes(tag_hash, 'big')
        return tag_int