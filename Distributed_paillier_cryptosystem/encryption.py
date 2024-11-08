import random
from gmpy2 import mpz, invert
random.seed(42)

class DPC:
    def __init__(self, p=3796265857, q=4043567029):
        self.p = mpz(p)
        self.q = mpz(q)
        self.N = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.public_key = self.N
        self.private_key = invert(self.N, self.phi)

    def encrypt(self, plaintext):
        r = mpz(random.randint(1, self.N - 1))
        ciphertext = (pow(r, self.N, self.N**2) * (1 + self.N * plaintext)) % self.N**2
        return ciphertext

    def decrypt(self, ciphertext):
        m = pow(ciphertext, self.private_key, self.N**2) - 1
        plaintext = m // self.N
        return int(plaintext)  # Ensure plaintext is an integer

    def split_private_key(self, n_shares, threshold):
        shares = []
        coefficients = [self.private_key] + [random.randint(1, self.N - 1) for _ in range(threshold - 1)]

        for i in range(1, n_shares + 1):
            y = sum(c * pow(i, j) for j, c in enumerate(coefficients)) % self.N
            shares.append((i, y))

        return shares

    def combine_shares(self, partial_decryptions):
        product = 1
        for partial_decryption in partial_decryptions:
            product *= partial_decryption
        product %= self.N**2
        return self.decrypt(product)

    def partial_decrypt(self, ciphertext, partial_key):
        partial_key_int, *_ = partial_key
        partial_decryption = pow(ciphertext, partial_key_int, self.N**2)
        return partial_decryption


plain1 = 142
plain2 = 152

Obj = DPC()
Ind = Obj.split_private_key(2, 2)
print(Ind)
cipher1 = Obj.encrypt(plain1)
cipher2 = Obj.encrypt(plain2)
partial1 = Obj.partial_decrypt(cipher1, Ind[0])
print(cipher1)
print(Obj.decrypt(cipher1))
partial2 = Obj.partial_decrypt(cipher2, Ind[1])
print(cipher2)
print(Obj.decrypt(cipher2))
product = Obj.combine_shares([partial1, partial2])
print(product)
