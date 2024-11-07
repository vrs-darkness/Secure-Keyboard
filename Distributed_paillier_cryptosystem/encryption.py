import math
import random
# random.seed(45)


class DPC:
    def __init__(self, p=3796265857, q=4043567029):
        self.p = p
        self.q = q
        self.public = None
        self.private = None
        self.delta = None
        self.partial_keys = []

    def KeyGeneration(self):
        """Generates the public and private keys"""
        N = self.p * self.q
        Zt = math.lcm(self.p - 1, self.q - 1)
        self.public = N
        self.private = Zt

    def extended_gcd(self, a, b):
        """Return gcd, x, y such that ax + by = gcd(a, b)"""
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def mod_inverse(self, a, m):
        """Return the modular inverse of a under modulo m"""
        gcd, x, _ = self.extended_gcd(a, m)
        if gcd != 1:
            raise ValueError("Inverse does not exist")
        return x % m

    def find_delta(self):
        """Find delta that satisfies the conditions"""
        k1 = self.mod_inverse(self.private, self.public)
        delta = k1 * self.private
        self.delta = delta
        return delta

    def PrivateSplit(self, Nclients, threshold):
        """Splits the private key into partial keys for each participant"""
        if self.delta is None:
            self.find_delta()

        # Define the polynomial coefficients
        coefficients = [self.delta] + [random.randint(1, self.public) for _ in range(threshold - 1)]
        # Generate partial private keys for each client
        for i in range(1, Nclients + 1):
            partial_key = sum(coef * (i ** idx) for idx, coef in enumerate(coefficients)) % self.public
            self.partial_keys.append(partial_key)

    def Encrypt(self, plaintext):
        """Encrypts the plaintext message"""
        if self.public is None:
            raise ValueError("Public key not generated. Run KeyGeneration first.")

        r = random.randint(1, self.public - 1)
        ciphertext = ((1 + plaintext * self.public) * pow(r, self.public, self.public**2)) % (self.public ** 2)
        return ciphertext

    def PartialDecrypt(self, ciphertext, client_index):
        """Partially decrypts the ciphertext with a specific client's partial key"""
        if not self.partial_keys:
            raise ValueError("Partial keys not generated. Run PrivateSplit first.")
        partial_key = self.partial_keys[client_index]
        partial_decryption = pow(ciphertext, partial_key, self.public**2)
        return partial_decryption

    def CombinePartialDecryptions(self, partial_decryptions):
        """Combines partial decryptions to retrieve the original plaintext"""
        result = 1
        for pd in partial_decryptions:
            result *= pd
        result = result % (self.public**2)
        # This assumes an additional decoding step (if needed) to retrieve the plaintext
        return result


Obj = DPC()

Obj.KeyGeneration()
Obj.PrivateSplit(3, 10)
Text = "Hello how are you"
Data = int(''.join([str(ord(i)) for i in Text]))
Sum = 1
for i in Text:
    Sum *= ord(i)
print(Sum)
print(Data)
data = Obj.Encrypt(Data)
print(data)
partial = []
for i in range(3):
    partial.append(Obj.PartialDecrypt(data, i))
print(Obj.CombinePartialDecryptions(partial))
