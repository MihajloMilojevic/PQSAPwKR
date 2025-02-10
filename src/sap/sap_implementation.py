import pandas as pd
from Crypto.Hash import SHA3_256
import kyber
from Crypto.Random import get_random_bytes
import os

# Generate stealth address
def generate_stealth_address(rk, key, pk):
    hash_input = rk + key + pk
    hash_obj = SHA3_256.new(hash_input)
    stealth_address = hash_obj.digest()
    return stealth_address

# Register recipient's public key
def register_recipient(recipient_id, public_key, registry_file="registry.csv"):
    # Check if the file exists, and create it with the correct columns if it doesn't
    if not os.path.exists(registry_file):
        registry = pd.DataFrame(columns=["Recipient ID", "Public Key"])
        registry.to_csv(registry_file, index=False)
    else:
        registry = pd.read_csv(registry_file)
    
    # Check if the recipient is already registered
    if recipient_id in registry["Recipient ID"].values:
        print(f"Recipient {recipient_id} already registered.")
    else:
        # Append the new recipient to the registry
        registry = registry.append({"Recipient ID": recipient_id, "Public Key": public_key.hex()}, ignore_index=True)
        registry.to_csv(registry_file, index=False)
        print(f"Recipient {recipient_id} registered successfully.")

# Retrieve recipient's public key
def retrieve_public_key(recipient_id, registry_file="registry.csv"):
    if not os.path.exists(registry_file):
        raise FileNotFoundError(f"Registry file {registry_file} not found.")
    
    registry = pd.read_csv(registry_file)
    recipient = registry[registry["Recipient ID"] == recipient_id]
    if recipient.empty:
        raise ValueError(f"Recipient {recipient_id} not found in registry.")
    return bytes.fromhex(recipient["Public Key"].values[0])

# Register ephemeral public key
def register_ephemeral_key(ciphertext, view_tag, ephemeral_registry_file="ephemeral_registry.csv"):
    # Check if the file exists, and create it with the correct columns if it doesn't
    if not os.path.exists(ephemeral_registry_file):
        ephemeral_registry = pd.DataFrame(columns=["Ciphertext", "View Tag"])
        ephemeral_registry.to_csv(ephemeral_registry_file, index=False)
    else:
        ephemeral_registry = pd.read_csv(ephemeral_registry_file)
    
    # Append the new ephemeral key to the registry
    ephemeral_registry = ephemeral_registry.append({"Ciphertext": ciphertext.hex(), "View Tag": view_tag.hex()}, ignore_index=True)
    ephemeral_registry.to_csv(ephemeral_registry_file, index=False)
    print("Ephemeral key registered successfully.")

# Scan for stealth address (recipient's side)
def scan_for_stealth_address(private_key, ephemeral_registry_file="ephemeral_registry.csv"):
    if not os.path.exists(ephemeral_registry_file):
        raise FileNotFoundError(f"Ephemeral registry file {ephemeral_registry_file} not found.")
    
    ephemeral_registry = pd.read_csv(ephemeral_registry_file)
    for index, row in ephemeral_registry.iterrows():
        ciphertext = bytes.fromhex(row["Ciphertext"])
        view_tag = bytes.fromhex(row["View Tag"])
        
        # Decapsulate the ciphertext using the recipient's private key
        shared_key = kyber.Kyber512.decaps(private_key, ciphertext)
        if shared_key == view_tag:
            print(f"Stealth address found at index {index}.")
            return shared_key
    print("No matching stealth address found.")
    return None

# Example usage
if __name__ == "__main__":
    # Step 1: Key Generation using Kyber512
    pk, sk = kyber.Kyber512.keygen()
    
    # Step 2: Registering the Recipient’s public key
    recipient_id = "Alice"
    register_recipient(recipient_id, pk)
    
    # Step 3: Retrieving the Recipient’s public key
    pk_retrieved = retrieve_public_key(recipient_id)
    
    # Step 4: Encapsulation of the secret using Kyber512
    shared_key, ciphertext = kyber.Kyber512.encaps(pk_retrieved)  # Corrected method call
    
    # Step 5: Computing the Stealth Address
    rk = get_random_bytes(32)  # Some unique value related to the recipient
    stealth_address = generate_stealth_address(rk, shared_key, pk_retrieved)
    
    # Step 6: Registering the Ephemeral public key
    register_ephemeral_key(ciphertext, shared_key)
    
    # Step 7: Scanning for the Stealth Address (Recipient’s side)
    retrieved_shared_key = scan_for_stealth_address(sk)
    
    if retrieved_shared_key:
        # Step 8: Deriving the Private stealth key
        private_stealth_key = generate_stealth_address(rk, retrieved_shared_key, pk_retrieved)
        print("Private stealth key derived successfully.")
        # Step 9: Completing the Stealth Address Protocol
        print("Stealth address protocol completed.")