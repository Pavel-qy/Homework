# Task 6.3
#
# Implement The Keyword encoding and decoding for latin alphabet.
# The Keyword Cipher uses a Keyword to rearrange the letters in the alphabet.
# Add the provided keyword at the begining of the alphabet.
# A keyword is used as the key, and it determines the letter matchings of the 
# cipher alphabet to the plain alphabet. 
# Repeats of letters in the word are removed, then the cipher alphabet 
# is generated with the keyword matching to A, B, C etc. until the keyword 
# is used up, whereupon the rest of the ciphertext letters are used in alphabetical order, 
# excluding those already used in the key.
#
# Encryption:
# Keyword is "Crypto"
#
# * A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
# * C R Y P T O A B D E F G H I J K L M N Q S U V W X Z


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
