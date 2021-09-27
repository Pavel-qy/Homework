# Task 6.3
class Cipher:
    """
    The Cipher object contain encoding and decoding methods for latin alphabet.
    A keyword is used as the key, and it determines the letter matchings of
    the cipher alphabet to the plain alphabet.
    """
    def __init__(self, keyword):
        self.keyword = keyword.lower()
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.cipher = alphabet
        for c in self.keyword:
            self.cipher = self.cipher.replace(c, "")
        self.cipher = self.keyword + self.cipher
        self.dict_encode = dict(zip(alphabet, self.cipher))
        self.dict_decode = dict(zip(self.cipher, alphabet))
    
    def encode(self, text):
        self.text = list(text.lower())
        for i, char in enumerate(self.text):
            if char.isalpha():
                self.text[i] = self.dict_encode[char]
        print("".join(self.text).capitalize())
    
    def decode(self, text):
        self.text = list(text.lower())
        for i, char in enumerate(self.text):
            if char.isalpha():
                self.text[i] = self.dict_decode[char]
        print("".join(self.text).capitalize())


cipher = Cipher("crypto")
cipher.encode("Hello world")
cipher.decode("Fjedhc dn atidsn")
