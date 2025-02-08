import kyber
import csv
from hashlib import sha3_256

class ModuleLWESAP:
    def __init__(self, registry_file="registry.csv"):
        """Initialize the Module-LWE SAP with a CSV-based ENS registry."""
        self.registry_file = registry_file
        self.ephemeral_key_registry = {}
    
    def key_generation(self):
        """Generate recipient's key pairs."""
        pk, sk = kyber.Kyber512.keygen()
        return pk, sk
    
    def register_meta_address(self, recipient_id, pk):
        """Register recipient's public key in a CSV file."""
        existing_pk = self.retrieve_meta_address(recipient_id)
        if existing_pk:
            raise ValueError(f"Recipient ID {recipient_id} already exists in the registry.")
        with open(self.registry_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([recipient_id, str(pk)])  # Store bytes as a string representation
    
    def retrieve_meta_address(self, recipient_id):
        """Retrieve recipient's public key from the CSV registry."""
        try:
            with open(self.registry_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == recipient_id:
                        # Convert the public key from string to bytes
                        return eval(row[1])  # Use eval to convert string representation of bytes back to bytes
        except FileNotFoundError:
            return None
        return None
    
    def encapsulate_secret(self, pk):
        """Generate shared secret and ephemeral public key."""
        if not isinstance(pk, bytes):
            raise TypeError("Public key must be in bytes.")
        c, key = kyber.Kyber512.enc(pk)
        
        # Debugging: Print ciphertext length and raw ciphertext
        print(f"Ciphertext Length: {len(c)} bytes")
        print(f"Raw Ciphertext: {c}")
        
        return c, key
    
    def compute_stealth_address(self, rhoK, key, tK):
        """Compute the recipient's stealth address."""
        if not isinstance(rhoK, bytes):
            rhoK = rhoK.encode()
        if not isinstance(tK, bytes):
            tK = tK.encode()
        
        xof_rhoK = int.from_bytes(sha3_256(rhoK).digest(), 'big')
        xof_key = int.from_bytes(sha3_256(key).digest(), 'big')
        tK_int = int.from_bytes(tK, 'big')
        
        # Ensure arithmetic operations are valid
        P = (xof_rhoK * xof_key + tK_int) % (2**256)  # Example: Use modulo to prevent overflow
        return P

    def register_ephemeral_key(self, c, key):
        """Register the ephemeral public key and view tag.""" 
        view_tag = sha3_256(key).digest()[:4]  # Use first 4 bytes for view tag
        self.ephemeral_key_registry[c] = view_tag
        # Save to file
        with open("ephemeral_keys.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([c, view_tag])
    
    def scan_for_stealth_address(self, sk):
        """Scan ephemeral key registry for matching stealth addresses."""
        for ci, view_tag in self.ephemeral_key_registry.items():
            # Debugging: Check size of ciphertext passed to dec
            print(f"Ciphertext passed to dec: Length = {len(ci)} bytes")
            print(f"Ciphertext passed to dec (raw): {ci}")
            
            # Ensure ciphertext is correctly sized for Kyber512
            if len(ci) != 768:  # Kyber512 ciphertext size
                raise ValueError("Invalid ciphertext length for Kyber512.")

            try:
                # Attempt to decrypt the ciphertext (decryption logic)
                key = kyber.Kyber512.dec(sk, ci)  # Decrypt ciphertext
                print(f"Decrypted Key: {key}")
            except Exception as e:
                print(f"Error during decryption: {e}")
                continue
            
            # Ensure the decrypted key matches the view tag
            if sha3_256(key).digest()[:4] == view_tag:
                return ci, key
        return None, None
    
    def derive_private_stealth_key(self, k, key):
        """Derive private key for stealth address."""
        xof_key = int.from_bytes(sha3_256(key).digest(), 'big')
        return k + xof_key

# Example usage
def test_mlwe_sap():
    protocol = ModuleLWESAP()
    
    # Step 1: Recipient generates keys
    pk, sk = protocol.key_generation()
    protocol.register_meta_address("Alice", pk)
    
    # Step 2: Sender retrieves recipient's public key
    recipient_pk = protocol.retrieve_meta_address("Alice")
    if not recipient_pk:
        print("Recipient not found.")
        return
    
    # Step 3-4: Sender encapsulates secret and computes stealth address
    c, key = protocol.encapsulate_secret(recipient_pk)
    
    # Convert `pk` to bytes for use as `tK`
    P = protocol.compute_stealth_address(recipient_pk, key, pk)
    protocol.register_ephemeral_key(c, key)
    
    # Step 5-6: Recipient scans for their stealth address
    cj, kj = protocol.scan_for_stealth_address(sk)
    if cj:
        print("Stealth address discovered!")
        p = protocol.derive_private_stealth_key(sk, kj)
        print("Derived private key for stealth address:", p)
    else:
        print("No matching stealth address found.")

if __name__ == "__main__":
    test_mlwe_sap()