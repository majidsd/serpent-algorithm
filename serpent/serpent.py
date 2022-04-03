import helper as help_functions
import constants as constants_values

class serpant:
    def __init__(self,key):
        key = key.encode('hex')
        bitsInKey = help_functions.keyLengthInBitsOf(key)
        rawKey = help_functions.convertToBitstring(help_functions.reverse(key.lower()), bitsInKey)
        self.userKey = help_functions.makeLongKey(rawKey)

    def encrypt(self,block):
        plainText = help_functions.convertToBitstring(help_functions.reverse(block.encode("hex").lower()), 128)
        cipherText = encrypt(plainText, self.userKey)
        return help_functions.reverse(help_functions.bitstring2hexstring(cipherText)).decode('hex')

    def decrypt(self,block):
        cipherText = help_functions.convertToBitstring(help_functions.reverse(block.encode("hex").lower()), 128)
        plainText = decrypt(cipherText, self.userKey)
        return help_functions.reverse(help_functions.bitstring2hexstring(plainText)).decode('hex')

    def get_block_size(self):
        return 16

def encrypt(plainText, userKey):
    """Encrypt the 128-bit bitstring 'plainText' with the 256-bit bitstring
    'userKey', using the normal algorithm, and return a 128-bit ciphertext
    bitstring."""

    K, KHat = help_functions.makeSubkeys(userKey)

    BHat = help_functions.IP(plainText) # BHat_0 at this stage
    for i in range(constants_values.r):
        BHat = help_functions.R(i, BHat, KHat) # Produce BHat_i+1 from BHat_i
    # BHat is now _32 i.e. _r
    C = help_functions.FP(BHat)

    return C

def decrypt(cipherText, userKey):
    """Decrypt the 128-bit bitstring 'cipherText' with the 256-bit
    bitstring 'userKey', using the normal algorithm, and return a 128-bit
    plaintext bitstring."""

    K, KHat = help_functions.makeSubkeys(userKey)

    BHat = help_functions.FPInverse(cipherText) # BHat_r at this stage
    for i in range(constants_values.r-1, -1, -1): # from r-1 down to 0 included
        BHat = help_functions.RInverse(i, BHat, KHat) # Produce BHat_i from BHat_i+1
    # BHat is now _0
    plainText = help_functions.IPInverse(BHat)

    return plainText


def encryptBitslice(plainText, userKey):
    """Encrypt the 128-bit bitstring 'plainText' with the 256-bit bitstring
    'userKey', using the bitslice algorithm, and return a 128-bit ciphertext
    bitstring."""

    K, KHat = help_functions.makeSubkeys(userKey)

    B = plainText # B_0 at this stage
    for i in range(constants_values.r):
        B = help_functions.RBitslice(i, B, K) # Produce B_i+1 from B_i
    # B is now _r

    return B


def decryptBitslice(cipherText, userKey):
    """Decrypt the 128-bit bitstring 'cipherText' with the 256-bit
    bitstring 'userKey', using the bitslice algorithm, and return a 128-bit
    plaintext bitstring."""

    K, KHat = help_functions.makeSubkeys(userKey)

    B = cipherText # B_r at this stage
    for i in range(constants_values.r-1, -1, -1): # from r-1 down to 0 included
        B = help_functions.RBitsliceInverse(i, B, K) # Produce B_i from B_i+1
    # B is now _0
    
    return B