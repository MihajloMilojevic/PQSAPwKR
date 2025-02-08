import numpy as np

def generate_mlwe_samples(n, q, m, error_std):
    """
    Generates MLWE samples with enhanced security and efficiency.
    
    :param n: Dimension of the polynomial ring
    :param q: Prime modulus
    :param m: Number of samples
    :param error_std: Standard deviation of error distribution
    :return: (A, b, s) where A is the public matrix, b is the noisy output, and s is the secret
    """
    np.random.seed(42) 
    
    s = np.random.randint(0, q, size=n)
    
    A = np.random.randint(0, q, size=(m, n))
    
    e = np.round(np.random.normal(0, error_std, size=m)).astype(int) % q
    
    b = (A @ s + e) % q
    
    return A, b, s

def generate_random_vectors(m, q):
    """
    Generates purely random vectors for comparison.
    
    :param m: Number of samples
    :param q: Prime modulus
    :return: Randomly generated vector b
    """
    return np.random.randint(0, q, size=m)

def validate_mlwe_samples(A, b, s, q, error_std):
    """
    Validates the generated MLWE samples by checking the consistency of b.
    
    :param A: Public matrix
    :param b: Noisy output vector
    :param s: Secret vector
    :param q: Prime modulus
    :param error_std: Standard deviation of error
    :return: Boolean indicating if validation is successful
    """
    expected_b = (A @ s) % q
    
    error = (b - expected_b + q // 2) % q - q // 2
    
    return np.all(np.abs(error) <= 3 * error_std)  

def differentiate_mlwe_random(b_mlwe, b_random):
    """
    Tests if we can differentiate between MLWE-generated vectors and purely random vectors.
    
    :param b_mlwe: MLWE-generated vector
    :param b_random: Randomly generated vector
    :return: Boolean indicating if differentiation is possible
    """
    mean_mlwe = np.mean(b_mlwe)
    mean_random = np.mean(b_random)
    std_mlwe = np.std(b_mlwe)
    std_random = np.std(b_random)
    
    return abs(mean_mlwe - mean_random) > 1.5 or abs(std_mlwe - std_random) > 1.5

def test_mlwe():
    """
    Tests the MLWE sample generation with multiple test cases and differentiation tests.
    """
    test_cases = [
        (4, 97, 6, 3),  
        (5, 101, 8, 4), 
        (3, 89, 5, 2)   
    ]
    
    for i, (n, q, m, e_std) in enumerate(test_cases):
        print(f"Running Test Case {i+1}: n={n}, q={q}, m={m}, e_std={e_std}")
        A, b_mlwe, s = generate_mlwe_samples(n, q, m, e_std)
        b_random = generate_random_vectors(m, q)
        valid = validate_mlwe_samples(A, b_mlwe, s, q, e_std)
        diff_result = differentiate_mlwe_random(b_mlwe, b_random)
        
        print("Public matrix A:", A)
        print("Noisy output vector b (MLWE):", b_mlwe)
        print("Random vector b:", b_random)
        print("Secret vector s:", s)
        print("Validation result:", "PASS" if valid else "FAIL")
        print("Can differentiate MLWE from random:", "YES" if diff_result else "NO")
        print("-" * 50)

if __name__ == "__main__":
    test_mlwe()