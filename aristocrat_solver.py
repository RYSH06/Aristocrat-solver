import random
import math
import sys

class AristocratSolver:
    def __init__(self, quadgram_file="english-quadgrams.txt"):
        self.quadgrams = {}
        self.total_count = 0
        self.min_probability = 0
        self.alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self._load_quadgrams(quadgram_file)

    def _load_quadgrams(self, filename):
        """ load 4-letter sequence from the file """
        try:
            # read file, add key and count to the map
            with open(filename, "r") as f:
                for line in f:
                    parts = line.split()
                    if len(parts) == 2:
                        key = parts[0]
                        count = int(parts[1])
                        self.quadgrams[key] = count
                        self.total_count += count

            # Convert to count to log probability for calculation
            for key in self.quadgrams:
                probability = self.quadgrams[key] / self.total_count
                self.quadgrams[key] = math.log10(probability)

            self.min_probability = math.log10(0.01 / self.total_count)

        except FileNotFoundError:
            print(f"Error: '{filename}' not found.")
            sys.exit(1)

    def get_fitness(self, text):
        """ scores text based on quadgram window """
        score = 0
        clean_text = "".join([c for c in text if c.isalpha()]).upper()

        if len(clean_text) < 4:
            return self.min_probability * len(clean_text)

        for i in range(len(clean_text) - 3):
            quad = clean_text[i:i+4]
            score += self.quadgrams.get(quad, self.min_probability)

        return score

    def decipher(self, ciphertext, key_mapping):
        """ applies the substitution key to the ciphertext """
        key_str = "".join(key_mapping)
        trans_table = str.maketrans("".join(self.alphabet), key_str)
        return ciphertext.translate(trans_table)

    def solve(self, ciphertext):
        ciphertext = ciphertext.upper()
        best_global_key = None
        best_global_score = -float('inf')
        best_global_text = ""

        for i in range(50):
            parent_key = list(self.alphabet)
            random.shuffle(parent_key)
            parent_text = self.decipher(ciphertext, parent_key)
            parent_score = self.get_fitness(parent_text)
            count = 0
            # Hill Climb Loop
            while count < 2500:
                child_key = parent_key[:]

                # Mutation: Swap two random letters
                a = random.randint(0, 25)
                b = random.randint(0, 25)
                child_key[a], child_key[b] = child_key[b], child_key[a]
                child_text = self.decipher(ciphertext, child_key)
                child_score = self.get_fitness(child_text)

                # Selection
                if child_score > parent_score:
                    parent_score = child_score
                    parent_key = child_key
                    count = 0 # Improvement found, reset counter
                else:
                    count += 1 # No improvement

            # Check global best
            if parent_score > best_global_score:
                best_global_score = parent_score
                best_global_key = parent_key
                best_global_text = self.decipher(ciphertext, parent_key)

        return best_global_text

if __name__ == "__main__":
    # Standard Aristocrat Cipher
    # (Solution: "THE LOOK OF THE JESSE OWENS REFEREE...")
    cipher_text = """
    JF XZ VWJFNVRSJZY VI JF AZZU IFGBVIJVRSJZY XKJ WFJ XZ SXUZ JF ISO VJ
    """
    
    # Ensure 'english_quadgrams.txt' is in the same folder
    solver = AristocratSolver('english-quadgrams.txt')
    result = solver.solve(cipher_text)
    
    print("\nFINAL DECRYPTION:")
    print(result)
