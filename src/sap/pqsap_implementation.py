import pandas as pd
from crypto.Hash import SHA3_256
from crypto.Random import get_random_bytes
import kyber
import os

def generate_stealth_address(rk, key, pk):
    hash_input = rk + key + pk
    hash_obj = SHA3_256.new(hash_input)
    stealth_address = hash_obj.digest()
    return stealth_address

def register_recipient(recipient_id, public_key, registry_file="registry.csv"):
    if not os.path.exists(registry_file):
        registry = pd.DataFrame(columns=["Recipient ID", "Public Key"])
        registry.to_csv(registry_file, index=False)
    else:
        registry = pd.read_csv(registry_file)
    
    if recipient_id in registry["Recipient ID"].values:
        print(f"Recipient {recipient_id} already registered.")
    else:
        registry = registry._append({"Recipient ID": recipient_id, "Public Key": public_key.hex()}, ignore_index=True)
        registry.to_csv(registry_file, index=False)
        print(f"Recipient {recipient_id} registered successfully.")

def retrieve_public_key(recipient_id, registry_file="registry.csv"):
    if not os.path.exists(registry_file):
        raise FileNotFoundError(f"Registry file {registry_file} not found.")
    
    registry = pd.read_csv(registry_file)
    recipient = registry[registry["Recipient ID"] == recipient_id]
    if recipient.empty:
        raise ValueError(f"Recipient {recipient_id} not found in registry.")
    return bytes.fromhex(recipient["Public Key"].values[0])

def register_ephemeral_key(ciphertext, view_tag, ephemeral_registry_file="ephemeral_registry.csv"):
    if not os.path.exists(ephemeral_registry_file):
        ephemeral_registry = pd.DataFrame(columns=["Ciphertext", "View Tag"])
        ephemeral_registry.to_csv(ephemeral_registry_file, index=False)
    else:
        ephemeral_registry = pd.read_csv(ephemeral_registry_file)
    
    ephemeral_registry = ephemeral_registry._append({"Ciphertext": ciphertext.hex(), "View Tag": view_tag.hex()}, ignore_index=True)
    ephemeral_registry.to_csv(ephemeral_registry_file, index=False)
    print("Ephemeral key registered successfully.")

def scan_for_stealth_address(private_key, ephemeral_registry_file="ephemeral_registry.csv"):
    if not os.path.exists(ephemeral_registry_file):
        raise FileNotFoundError(f"Ephemeral registry file {ephemeral_registry_file} not found.")
    
    ephemeral_registry = pd.read_csv(ephemeral_registry_file)
    for index, row in ephemeral_registry.iterrows():
        ciphertext = bytes.fromhex(row["Ciphertext"])
        view_tag = bytes.fromhex(row["View Tag"])
        
        shared_key = kyber.Kyber512.dec(ciphertext, private_key)
        if shared_key == view_tag:
            print(f"Stealth address found at index {index}.")
            return shared_key
    print("No matching stealth address found.")
    return None

def test_case_1():
    print("=== Test Case 1: Basic Functionality ===")
    pk, sk = kyber.Kyber512.keygen()
    print(f"Generated Public Key (first 16 bytes): {pk[:16].hex()}...")
    print(f"Generated Secret Key (first 16 bytes): {sk[:16].hex()}...")
    
    recipient_id = "Alice"
    register_recipient(recipient_id, pk)
    
    pk_retrieved = retrieve_public_key(recipient_id)
    print(f"Retrieved Public Key (first 16 bytes): {pk_retrieved[:16].hex()}...")
    
    ciphertext, shared_key = kyber.Kyber512.enc(pk_retrieved)
    print(f"Encapsulated Shared Key (first 16 bytes): {shared_key[:16].hex()}...")
    print(f"Ciphertext (first 16 bytes): {ciphertext[:16].hex()}...")
    
    rk = get_random_bytes(32)
    stealth_address = generate_stealth_address(rk, shared_key, pk_retrieved)
    print(f"Stealth Address (first 16 bytes): {stealth_address[:16].hex()}...")
    
    register_ephemeral_key(ciphertext, shared_key)
    
    retrieved_shared_key = scan_for_stealth_address(sk)
    if retrieved_shared_key:
        private_stealth_key = generate_stealth_address(rk, retrieved_shared_key, pk_retrieved)
        print(f"Private Stealth Key (first 16 bytes): {private_stealth_key[:16].hex()}...")
        print("Test Case 1 Passed - Stealth address protocol completed.")
    else:
        print("Test Case 1 Failed: No matching stealth address found.")
    print()

def test_case_2():
    print("=== Test Case 2: Multiple Recipients ===")
    pk_alice, sk_alice = kyber.Kyber512.keygen()
    print(f"Alice's Public Key (first 16 bytes): {pk_alice[:16].hex()}...")
    print(f"Alice's Secret Key (first 16 bytes): {sk_alice[:16].hex()}...")
    
    register_recipient("Alice", pk_alice)
    
    pk_bob, sk_bob = kyber.Kyber512.keygen()
    print(f"Bob's Public Key (first 16 bytes): {pk_bob[:16].hex()}...")
    print(f"Bob's Secret Key (first 16 bytes): {sk_bob[:16].hex()}...")
    
    register_recipient("Bob", pk_bob)
    
    ciphertext_alice, shared_key_alice = kyber.Kyber512.enc(pk_alice)
    ciphertext_bob, shared_key_bob = kyber.Kyber512.enc(pk_bob)
    
    register_ephemeral_key(ciphertext_alice, shared_key_alice)
    register_ephemeral_key(ciphertext_bob, shared_key_bob)
    
    print("Scanning for Alice's stealth address:")
    retrieved_shared_key_alice = scan_for_stealth_address(sk_alice)
    if retrieved_shared_key_alice:
        print("Alice's stealth address found.")
    else:
        print("Test Case 2 Failed: Alice's stealth address not found.")
    
    print("Scanning for Bob's stealth address:")
    retrieved_shared_key_bob = scan_for_stealth_address(sk_bob)
    if retrieved_shared_key_bob:
        print("Bob's stealth address found.")
    else:
        print("Test Case 2 Failed: Bob's stealth address not found.")
    print()

def test_case_3():
    print("=== Test Case 3: Invalid Ciphertext ===")
    pk, sk = kyber.Kyber512.keygen()
    print(f"Generated Public Key (first 16 bytes): {pk[:16].hex()}...")
    print(f"Generated Secret Key (first 16 bytes): {sk[:16].hex()}...")
    
    recipient_id = "Alice"
    register_recipient(recipient_id, pk)
    
    pk_retrieved = retrieve_public_key(recipient_id)
    print(f"Retrieved Public Key (first 16 bytes): {pk_retrieved[:16].hex()}...")
    
    ciphertext, shared_key = kyber.Kyber512.enc(pk_retrieved)
    print(f"Encapsulated Shared Key (first 16 bytes): {shared_key[:16].hex()}...")
    print(f"Ciphertext (first 16 bytes): {ciphertext[:16].hex()}...")
    
    invalid_ciphertext = get_random_bytes(768)
    register_ephemeral_key(invalid_ciphertext, shared_key)
    
    retrieved_shared_key = scan_for_stealth_address(sk)
    if retrieved_shared_key:
        print("Test Case 3 Failed: Stealth address found with invalid ciphertext.")
    else:
        print("Test Case 3 Passed: No stealth address found with invalid ciphertext.")
    print()

if __name__ == "__main__":
    if os.path.exists("registry.csv"):
        os.remove("registry.csv")
    if os.path.exists("ephemeral_registry.csv"):
        os.remove("ephemeral_registry.csv")
    
    test_case_1()
    test_case_2()
    test_case_3()