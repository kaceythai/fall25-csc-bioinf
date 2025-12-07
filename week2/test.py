import os
import sys

try:
    if __codon__:
        pass
except NameError:
    __codon__ = False

# ---------------------------------------------------------
# 1. IMPORTS (Handle Codon vs Python differences)
# ---------------------------------------------------------
if __codon__:
    from code.bio_codon import motifs
    from code.bio_codon.motifs import matrix
    from code.bio_codon.motifs import thresholds
    # Codon handles floats slightly differently, so we use a custom check
else:
    # Set path so we can find the local 'code' folder
    sys.path.append("code") 
    from bio_codon import motifs
    from bio_codon.motifs import matrix
    from bio_codon.motifs import thresholds
    
    # Python doesn't have the @test decorator, so we make a dummy one
    def test(func):
        return func

# ---------------------------------------------------------
# 2. HELPER FUNCTIONS
# ---------------------------------------------------------
def assert_equal(actual, expected, message=""):
    if actual != expected:
        print(f"FAIL: {message} | Expected {expected}, got {actual}")
        sys.exit(1)
    else:
        print(f"PASS: {message}")

def assert_almost_equal(actual, expected, tolerance=1e-5, message=""):
    diff = abs(actual - expected)
    if diff > tolerance:
        print(f"FAIL: {message} | Expected {expected}, got {actual} (diff: {diff})")
        sys.exit(1)
    else:
        print(f"PASS: {message}")

# ---------------------------------------------------------
# 3. TEST DATA (Minimal MEME Format)
# ---------------------------------------------------------
# We create a dummy file content so we don't need external files
MINIMAL_FILE_CONTENT = """MEME version 4

ALPHABET= ACGT

strands: + -

Background letter frequencies
A 0.25 C 0.25 G 0.25 T 0.25

MOTIF 1 TestMotif
letter-probability matrix: alength= 4 w= 4 nsites= 10 E= 0
 1.0 0.0 0.0 0.0 
 0.0 1.0 0.0 0.0 
 0.0 0.0 1.0 0.0 
 0.0 0.0 0.0 1.0 
"""

# ---------------------------------------------------------
# 4. TESTS
# ---------------------------------------------------------

@test
def test_minimal_parsing():
    print("\n--- Testing Minimal Parser ---")
    filename = "temp_test_minimal.meme"
    
    # 1. Create a temporary file
    with open(filename, "w") as f:
        f.write(MINIMAL_FILE_CONTENT)
    
    # 2. Parse it using your ported code
    try:
        with open(filename, "r") as handle:
            # This calls minimal.read() internally
            record = motifs.parse(handle, "minimal")
        
        # 3. Verify results
        assert_equal(len(record), 1, "Should find 1 motif")
        
        m = record[0]
        assert_equal(m.name, "TestMotif", "Check Motif Name")
        assert_equal(m.length, 4, "Check Motif Length")
        assert_equal(m.alphabet, "ACGT", "Check Alphabet")
        
    finally:
        # Clean up the file
        if os.path.exists(filename):
            os.remove(filename)

@test
def test_matrix_calculation():
    print("Testing Matrix Calculation (PSSM) ")

    alphabet = "ACGT"
    counts = {
        "A": [10.0, 0.0, 0.0, 0.0],
        "C": [0.0, 10.0, 0.0, 0.0],
        "G": [0.0, 0.0, 10.0, 0.0],
        "T": [0.0, 0.0, 0.0, 10.0]
    }
    m = motifs.Motif(alphabet, counts=counts)
    pssm = m.pssm
    seq_match = "ACGT"
    score_match = pssm.calculate(seq_match)
    val = 0.0
    try:
        val = float(score_match[0])
    except:
        val = float(score_match)

    print(f"Score for matching sequence: {val}")
    if val <= 0:
        print("FAIL: Matching sequence should have positive score")
        sys.exit(1)
    else:
        print("PASS: Matching sequence score is positive")

@test
def test_thresholds():
    print("\nTesting Thresholds (ScoreDistribution) ")
    alphabet = "ACGT"
    counts = {
        "A": [10, 0],
        "C": [0, 10],
        "G": [0, 0],
        "T": [0, 0]
    }
    m = motifs.Motif(alphabet, counts=counts)
    m.pseudocounts = 1.0
    sd = thresholds.ScoreDistribution(pssm=m.pssm, background=m.background)

    max_score = sd.interval + sd.min_score
    print(f"Max score calculated: {max_score}")

    if max_score > 0:
        print("PASS: Threshold distribution calculated")
    else:
        print("FAIL: Threshold distribution invalid")

if __name__ == "__main__":
    test_minimal_parsing()
    test_matrix_calculation()
    test_thresholds()
    print("\nAll Tests Passed!")
