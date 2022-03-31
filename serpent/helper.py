import sys
import re
import random

import constants as constants_values

def key_gen(size=32):
    key = ''
    x = round(random.uniform(0, 1), 3)
    r = round(random.uniform(0, 4), 3)

    for i in range(size):
        x=r*x*(1-x) #logistic map
        key += convert_decimel_to_hexa(int((x*pow(10,16))%256)) #key=(x*10^16)%256
    return key

def convert_decimel_to_hexa(decimalValue):
    return hex(decimalValue).replace('0x', '')


def convert_decimel_to_binary64(decimalValue):
    return str(dec_to_bin(decimalValue)).zfill(64)

def dec_to_bin(x):
    return int(bin(x)[2:])

def random_iv(length):
    iv = ""
    for i in range(length):
        iv +=  str(random.randint(0, 1))
    return iv

def reverse(toreverse):
    out = ""
    for i in range(int((len(toreverse)/2))):
        out += toreverse[len(toreverse)-i*2-2:len(toreverse)-i*2]
    return out


def S(box, input):
    """Apply S-box number 'box' to 4-bit bitstring 'input' and return a
    4-bit bitstring as the result."""

    return SBoxBitstring[box%8][input]
    # There used to be 32 different S-boxes in serpent-0. Now there are
    # only 8, each of which is used 4 times (Sboxes 8, 16, 24 are all
    # identical to Sbox 0, etc). Hence the %8.


def SInverse(box, output):
    """Apply S-box number 'box' in reverse to 4-bit bitstring 'output' and
    return a 4-bit bitstring (the input) as the result."""

    return SBoxBitstringInverse[box%8][output]


def SHat(box, input):
    """Apply a parallel array of 32 copies of S-box number 'box' to the
    128-bit bitstring 'input' and return a 128-bit bitstring as the
    result."""
    
    result = ""
    for i in range(32):
        result = result + S(box, input[4*i:4*(i+1)])
    return result


def SHatInverse(box, output):
    """Apply, in reverse, a parallel array of 32 copies of S-box number
    'box' to the 128-bit bitstring 'output' and return a 128-bit bitstring
    (the input) as the result."""

    result = ""
    for i in range(32):
        result = result + SInverse(box, output[4*i:4*(i+1)])
    return result


def SBitslice(box, words):
    """Take 'words', a list of 4 32-bit bitstrings, least significant word
    first. Return a similar list of 4 32-bit bitstrings obtained as
    follows. For each bit position from 0 to 31, apply S-box number 'box'
    to the 4 input bits coming from the current position in each of the
    items in 'words'; and put the 4 output bits in the corresponding
    positions in the output words."""

    result = ["", "", "", ""]
    for i in range(32): # ideally in parallel
        quad = S(box, words[0][i] + words[1][i] + words[2][i] + words[3][i])
        for j in range(4):
            result[j] = result[j] + quad[j]
    return result


def SBitsliceInverse(box, words):
    """Take 'words', a list of 4 32-bit bitstrings, least significant word
    first. Return a similar list of 4 32-bit bitstrings obtained as
    follows. For each bit position from 0 to 31, apply S-box number 'box'
    in reverse to the 4 output bits coming from the current position in
    each of the items in the supplied 'words'; and put the 4 input bits in
    the corresponding positions in the returned words."""

    result = ["", "", "", ""]
    for i in range(32): # ideally in parallel
        quad = SInverse(
            box, words[0][i] + words[1][i] + words[2][i] + words[3][i])
        for j in range(4):
            result[j] = result[j] + quad[j]
    return result


def LT(input):
    """Apply the table-based version of the linear transformation to the
    128-bit string 'input' and return a 128-bit string as the result."""

    if len(input) != 128:
        raise ValueError ("input to inverse LT is not 128 bit long")

    result = ""
    for i in range(len(constants_values.LTTable)):
        outputBit = "0"
        for j in constants_values.LTTable[i]:
            outputBit = xor(outputBit, input[j])
        result = result + outputBit
    return result


def LTInverse(output):
    """Apply the table-based version of the inverse of the linear
    transformation to the 128-bit string 'output' and return a 128-bit
    string (the input) as the result."""

    if len(output) != 128:
        raise ValueError ("input to inverse LT is not 128 bit long")

    result = ""
    for i in range(len(constants_values.LTTableInverse)):
        inputBit = "0"
        for j in constants_values.LTTableInverse[i]:
            inputBit = xor(inputBit, output[j])
        result = result + inputBit
    return result


def LTBitslice(X):
    """Apply the equations-based version of the linear transformation to
    'X', a list of 4 32-bit bitstrings, least significant bitstring first,
    and return another list of 4 32-bit bitstrings as the result."""

    X[0] = rotateLeft(X[0], 13)
    X[2] = rotateLeft(X[2], 3)
    X[1] = xor(X[1], X[0], X[2])
    X[3] = xor(X[3], X[2], shiftLeft(X[0], 3))
    X[1] = rotateLeft(X[1], 1)
    X[3] = rotateLeft(X[3], 7)
    X[0] = xor(X[0], X[1], X[3])
    X[2] = xor(X[2], X[3], shiftLeft(X[1], 7))
    X[0] = rotateLeft(X[0], 5)
    X[2] = rotateLeft(X[2], 22)

    return X


def LTBitsliceInverse(X):
    """Apply, in reverse, the equations-based version of the linear
    transformation to 'X', a list of 4 32-bit bitstrings, least significant
    bitstring first, and return another list of 4 32-bit bitstrings as the
    result."""

    X[2] = rotateRight(X[2], 22)
    X[0] = rotateRight(X[0], 5)
    X[2] = xor(X[2], X[3], shiftLeft(X[1], 7))
    X[0] = xor(X[0], X[1], X[3])
    X[3] = rotateRight(X[3], 7)
    X[1] = rotateRight(X[1], 1)
    X[3] = xor(X[3], X[2], shiftLeft(X[0], 3))
    X[1] = xor(X[1], X[0], X[2])
    X[2] = rotateRight(X[2], 3)
    X[0] = rotateRight(X[0], 13)

    return X


def IP(input):
    """Apply the Initial Permutation to the 128-bit bitstring 'input'
    and return a 128-bit bitstring as the result."""

    return applyPermutation(constants_values.IPTable, input)


def FP(input):
    """Apply the Final Permutation to the 128-bit bitstring 'input'
    and return a 128-bit bitstring as the result."""

    return applyPermutation(constants_values.FPTable, input)


def IPInverse(output):
    """Apply the Initial Permutation in reverse."""

    return FP(output)


def FPInverse(output):
    """Apply the Final Permutation in reverse."""

    return IP(output)


def applyPermutation(permutationTable, input):
    """Apply the permutation specified by the 128-element list
    'permutationTable' to the 128-bit bitstring 'input' and return a
    128-bit bitstring as the result."""
   
    if len(input) != len(permutationTable):
        raise ValueError ("input size (%d) doesn't match perm table size (%d)"% (len(input), len(permutationTable)))
        
    result = ""
    for i in range(len(permutationTable)):
        result = result + input[permutationTable[i]]
    return result


def R(i, BHati, KHat):
    """Apply round 'i' to the 128-bit bitstring 'BHati', returning another
    128-bit bitstring (conceptually BHatiPlus1). Do this using the
    appropriately numbered subkey(s) from the 'KHat' list of 33 128-bit
    bitstrings."""

    #O.show("BHati", BHati, "(i=%2d) BHati" % i)

    xored = xor(BHati, KHat[i])
    #O.show("xored", xored, "(i=%2d) xored" % i)

    SHati = SHat(i, xored)
    #O.show("SHati", SHati, "(i=%2d) SHati" % i)

    if 0 <= i <= constants_values.r-2:
        BHatiPlus1 = LT(SHati)
    elif i == constants_values.r-1:
        BHatiPlus1 = xor(SHati, KHat[constants_values.r])
    else:
        raise ValueError ( "round %d is out of 0..%d range" % (i, constants_values.r-1))
    #O.show("BHatiPlus1", BHatiPlus1, "(i=%2d) BHatiPlus1" % i)

    return BHatiPlus1

def RInverse(i, BHatiPlus1, KHat):
    """Apply round 'i' in reverse to the 128-bit bitstring 'BHatiPlus1',
    returning another 128-bit bitstring (conceptually BHati). Do this using
    the appropriately numbered subkey(s) from the 'KHat' list of 33 128-bit
    bitstrings."""

    #O.show("BHatiPlus1", BHatiPlus1, "(i=%2d) BHatiPlus1" % i)

    if 0 <= i <= constants_values.r-2:
        SHati = LTInverse(BHatiPlus1)
    elif i == constants_values.r-1:
        SHati = xor(BHatiPlus1, KHat[constants_values.r])
    else:
        raise ValueError("round %d is out of 0..%d range" % (i, constants_values.r-1))
    #O.show("SHati", SHati, "(i=%2d) SHati" % i)

    xored = SHatInverse(i, SHati)
    #O.show("xored", xored, "(i=%2d) xored" % i)

    BHati = xor(xored, KHat[i])
    #O.show("BHati", BHati, "(i=%2d) BHati" % i)

    return BHati


def RBitslice(i, Bi, K):
    """Apply round 'i' (bitslice version) to the 128-bit bitstring 'Bi' and
    return another 128-bit bitstring (conceptually B i+1). Use the
    appropriately numbered subkey(s) from the 'K' list of 33 128-bit
    bitstrings."""

    #O.show("Bi", Bi, "(i=%2d) Bi" % i)

    # 1. Key mixing
    xored = xor (Bi, K[i])
    #O.show("xored", xored, "(i=%2d) xored" % i)

    # 2. S Boxes
    Si = SBitslice(i, quadSplit(xored))
    # Input and output to SBitslice are both lists of 4 32-bit bitstrings
    #O.show("Si", Si, "(i=%2d) Si" % i, "tlb")

    # 3. Linear Transformation
    if i == constants_values.r-1:
        # In the last round, replaced by an additional key mixing
        BiPlus1 = xor(quadJoin(Si), K[constants_values.r])
    else:
        BiPlus1 = quadJoin(LTBitslice(Si))
    # BIPlus1 is a 128-bit bitstring
    #O.show("BiPlus1", BiPlus1, "(i=%2d) BiPlus1" % i)

    return BiPlus1


def RBitsliceInverse(i, BiPlus1, K):
    """Apply the inverse of round 'i' (bitslice version) to the 128-bit
    bitstring 'BiPlus1' and return another 128-bit bitstring (conceptually
    B i). Use the appropriately numbered subkey(s) from the 'K' list of 33
    128-bit bitstrings."""

    #O.show("BiPlus1", BiPlus1, "(i=%2d) BiPlus1" % i)

    # 3. Linear Transformation
    if i == constants_values.r-1:
        # In the last round, replaced by an additional key mixing
        Si = quadSplit(xor(BiPlus1, K[constants_values.r]))
    else:
        Si = LTBitsliceInverse(quadSplit(BiPlus1))
    # SOutput (same as LTInput) is a list of 4 32-bit bitstrings

    #O.show("Si", Si, "(i=%2d) Si" % i, "tlb")

    # 2. S Boxes
    xored = SBitsliceInverse(i, Si)
    # SInput and SOutput are both lists of 4 32-bit bitstrings

    #O.show("xored", xored, "(i=%2d) xored" % i)

    # 1. Key mixing
    Bi = xor (quadJoin(xored), K[i])

    #O.show("Bi", Bi, "(i=%2d) Bi" % i)

    return Bi


def makeSubkeys(userKey):
    """Given the 256-bit bitstring 'userKey' (shown as K in the paper, but
    we can't use that name because of a collision with K[i] used later for
    something else), return two lists (conceptually K and KHat) of 33
    128-bit bitstrings each."""

    # Because in Python I can't index a list from anything other than 0,
    # I use a dictionary instead to legibly represent the w_i that are
    # indexed from -8.

    # We write the key as 8 32-bit words w-8 ... w-1
    # ENOTE: w-8 is the least significant word
    
    w = {}
   
    for i in range(-8, 0):
        w[i] = userKey[(i+8)*32:(i+9)*32]
        #O.show("wi", w[i], "(i=%2d) wi" % i)

    # We expand these to a prekey w0 ... w131 with the affine recurrence
    for i in range(132):
        w[i] = rotateLeft(xor(w[i-8], w[i-5], w[i-3], w[i-1],bitstring(constants_values.phi, 32), bitstring(i,32)),11)
        #O.show("wi", w[i], "(i=%2d) wi" % i)

    # The round keys are now calculated from the prekeys using the S-boxes
    # in bitslice mode. Each k[i] is a 32-bit bitstring.
    k = {}
    for i in range(constants_values.r+1):
        whichS = (constants_values.r + 3 - i) % constants_values.r
        k[0+4*i] = ""
        k[1+4*i] = ""
        k[2+4*i] = ""
        k[3+4*i] = ""
        for j in range(32): # for every bit in the k and w words
            # ENOTE: w0 and k0 are the least significant words, w99 and k99
            # the most.
            input = w[0+4*i][j] + w[1+4*i][j] + w[2+4*i][j] + w[3+4*i][j]
            output = S(whichS, input)
            for l in range(4):
                k[l+4*i] = k[l+4*i] + output[l]

    # We then renumber the 32 bit values k_j as 128 bit subkeys K_i.
    K = []
    for i in range(33):
        # ENOTE: k4i is the least significant word, k4i+3 the most.
        K.append(k[4*i] + k[4*i+1] + k[4*i+2] + k[4*i+3])

    # We now apply IP to the round key in order to place the key bits in
    # the correct column
    KHat = []
    for i in range(33):
        KHat.append(IP(K[i]))

        #O.show("Ki", K[i], "(i=%2d) Ki" % i)
        #O.show("KHati", KHat[i], "(i=%2d) KHati" % i)

    return K, KHat

def makeLongKey(k):
    """Take a key k in bitstring format. Return the long version of that
    key."""

    l = len(k)
    if l % 32 != 0 or l < 64 or l > 256:
        raise ValueError("Invalid key length (%d bits)" % l)
    if l == 256:
        return k
    else:
        return k + "1" + "0"*(256 -l -1)

def bitstring(n, minlen=1):
    """Translate n from integer to bitstring, padding it with 0s as
    necessary to reach the minimum length 'minlen'. 'n' must be >= 0 since
    the bitstring format is undefined for negative integers.  Note that,
    while the bitstring format can represent arbitrarily large numbers,
    this is not so for Python's normal integer type: on a 32-bit machine,
    values of n >= 2^31 need to be expressed as python long integers or
    they will "look" negative and won't work. E.g. 0x80000000 needs to be
    passed in as 0x80000000L, or it will be taken as -2147483648 instead of
    +2147483648L.
    EXAMPLE: bitstring(10, 8) -> "01010000"
    """

    if minlen < 1:
        raise ValueError("a bitstring must have at least 1 char")
    if n < 0:
        raise ValueError("bitstring representation undefined for neg numbers")

    result = ""
    while n > 0:
        if n & 1:
            result = result + "1"
        else:
            result = result + "0"
        n = n >> 1
    if len(result) < minlen:
        result = result + "0" * (minlen - len(result))
    return result


def binaryXor(n1, n2):
    """Return the xor of two bitstrings of equal length as another
    bitstring of the same length.
    EXAMPLE: binaryXor("10010", "00011") -> "10001"
    """
    
    if len(n1) != len(n2):
       
        raise ValueError("can't xor bitstrings of different " + "lengths (%d and %d)" % (len(n1), len(n2)))
    # We assume that they are genuine bitstrings instead of just random
    # character strings.

    result = ""
    
    for i in range(len(n1)):
        if n1[i] == n2[i]:
            result = result + "0"
        else:
            result = result + "1"
    return result


def xor(*args):
    """Return the xor of an arbitrary number of bitstrings of the same
    length as another bitstring of the same length.
    EXAMPLE: xor("01", "11", "10") -> "00"
    """

    if args == []:
        raise ValueError("at least one argument needed")

    result = args[0]
    for arg in args[1:]:
        result = binaryXor(result, arg)
    return result


def rotateLeft(input, places):
    """Take a bitstring 'input' of arbitrary length. Rotate it left by
    'places' places. Left means that the 'places' most significant bits are
    taken out and reinserted as the least significant bits. Note that,
    because the bitstring representation is little-endian, the visual
    effect is actually that of rotating the string to the right.
    EXAMPLE: rotateLeft("000111", 2) -> "110001"
    """

    p = places % len(input)
    return input[-p:] + input[:-p]


def rotateRight(input, places):
    return rotateLeft(input, -places)


def shiftLeft(input, p):
    """Take a bitstring 'input' of arbitrary length. Shift it left by 'p'
    places. Left means that the 'p' most significant bits are shifted out
    and dropped, while 'p' 0s are inserted in the the least significant
    bits. Note that, because the bitstring representation is little-endian,
    the visual effect is actually that of shifting the string to the
    right. Negative values for 'p' are allowed, with the effect of shifting
    right instead (i.e. the 0s are inserted in the most significant bits).
    EXAMPLE: shiftLeft("000111", 2) -> "000001"
             shiftLeft("000111", -2) -> "011100"
    """

    if abs(p) >= len(input):
        # Everything gets shifted out anyway
        return "0" * len(input)
    if p < 0:
        # Shift right instead
        return  input[-p:] + "0" * len(input[:-p])
    elif p == 0:
        return input
    else: # p > 0, normal case
        return "0" * len(input[-p:]) + input[:-p]


def shiftRight(input, p):
    """Take a bitstring 'input' and shift it right by 'p' places. See the
    doc for shiftLeft for more details."""

    return shiftLeft(input, -p)


def keyLengthInBitsOf(k):
    """Take a string k in I/O format and return the number of bits in it."""

    return len(k) * 4


def bitstring2hexstring(b):
    """Take bitstring 'b' and return the corresponding hexstring."""

    result = ""
    l = len(b)
    if l % 4:
        b = b + "0" * (4-(l%4))
    for i in range(0, len(str(b)), 4):
        result = result + constants_values.bin2hex[b[i:i+4]]
    return reverseString(result)


def hexstring2bitstring(h):
    """Take hexstring 'h' and return the corresponding bitstring."""
    
    result = ""
    for c in reverseString(h):
        result = result + constants_values.hex2bin[c]

    return result


def reverseString(s):
    l = list(s)
    l.reverse()
    return "".join(l)


def quadSplit(b128):
    """Take a 128-bit bitstring and return it as a list of 4 32-bit
    bitstrings, least significant bitstring first."""

    if len(b128) != 128:
        raise ValueError("must be 128 bits long, not " + len(b128))
    result = []
    for i in range(4):
        result.append(b128[(i*32):(i+1)*32])
    return result


def quadJoin(l4x32):
    """Take a list of 4 32-bit bitstrings and return it as a single 128-bit
    bitstring obtained by concatenating the internal ones."""

    if len(l4x32) != 4:
        raise ValueError("need a list of 4 bitstrings, not " + len(l4x32))

    return l4x32[0] + l4x32[1] + l4x32[2] + l4x32[3]


def convertToBitstring(input, numBits):
    """Take a string 'input', theoretically in std I/O format, but in
    practice liable to contain any sort of crap since it's user supplied,
    and return its bitstring representation, normalised to numBits
    bits. Raise the appropriate variant of ValueError (with explanatory
    message) if anything can't be done (this includes the case where the
    'input', while otherwise syntactically correct, can't be represented in
    'numBits' bits)."""

    input = input.lower()

    print('Input: ' + input) #Key = input
    
    if re.match("^[0-9a-f]+$", input):
        bitstring = hexstring2bitstring(input)
        #print('BitString: '+ bitstring) # Unknown = each number is 0000 bits for the key
    else:
        raise ValueError ("%s is not a valid hexstring" % input)

    # assert: bitstring now contains the bitstring version of the input

    #print(numBits)
    print(len(bitstring))
    #print('bitstring[numBits:]: '+ bitstring[numBits:])

    if len(bitstring) > numBits:
        # Last chance: maybe it's got some useless 0s...
        if re.match("^0+$", bitstring[numBits:]):
            bitstring = bitstring[:numBits]
        else:
            raise ValueError ("input too large to fit in %d bits" % numBits)
    else:
        bitstring = bitstring + "0" * (numBits-len(bitstring))

    return bitstring

def prepare(input):
    result = ""
    for c in reverseString(input.lower()):
        result = constants_values.ebin2hex[constants_values.hex2bin[c]] + result
    
    return reverseString(result)

SBoxBitstring = []
SBoxBitstringInverse = []
for line in constants_values.SBoxDecimalTable:
    dict = {}
    inverseDict = {}
    for i in range(len(line)):
        index = bitstring(i, 4)
        value = bitstring(line[i], 4)
        dict[index] = value
        inverseDict[value] = index
    SBoxBitstring.append(dict)
    SBoxBitstringInverse.append(inverseDict)

def helpExit(message = None):
    print (constants_values.help)
    if message:
        print ("ERROR:", message)
    sys.exit()