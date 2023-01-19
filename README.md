## About Serpent Algorithm

Serpent a symmetric block cipher, was designed for AES by Eli Biham (Technion Israeli
Institute of Technology), Ross Anderson (University of Cambridge Computer Laboratory)
and Lars Knudsen (University of Bergen, Norway), published on 1998, serpent designed
to provide users with the highest practical level of assurance that no shortcut attack will
be found. In this Algorithm, a 128-bit block is ciphered by using a key of length 256 bit
in 32 different rounds. The first 31 rounds are identical, consisting of the same sequence
of elementary operations, while the last round differs only in the key schedule. Instead
of mixing a single key like in the first 31 rounds, an additional key is mixed in the last
round. Hence 33 round keys are required in the whole process that are generated from the external key.
 The algorithm consists of three basic functions:
Initial permutation(IP) 
32 Round function
Final permutation (FP).
IP is applied on plain-text in order to rearrange the bits. The IP is given by [(i∗32)mod127].
Applying this to a plain-text, we get a data block B0. The round function is performed
32 times on Bi. The algorithm defines eight S-boxes (Si). Inside these rounds, each
data block Bi mixed with a sub key Ki (i.e. taking XOR), then pass (Bi ⊕ Ki) through
(S(imod8)) which is one of the eight S-boxes. After this, a linear transformation to the
[Si(Bi ⊕ Ki)] is applied to get Bi+1, where i = 0, 1, 2. . . 30. In the 32nd round (last
round) a 33rd key is XOR-ed instead of applying a linear transformation (LT). Now the
final permutation [(i ∗ 4)mod127] is applied to get the cipher text. 
B0 = IP(p)
Bi+1 = LT(S − boximod8(Bi ⊕ Ki))
Where i= 0, 1, 2. . . 30
B32 = S7(B31 ⊕ K31 ⊕ K32)
C = F P(B32).


## About CTR Mode

The Counter Mode or CTR is a simple counter based block cipher implementation in
cryptography. Each or every time a counter initiated value is encrypted and given as
input to XOR with plain-text or original text which results in a cipher-text block. The
CTR mode is independent of feedback use and thus can be implemented in parallel in this
mode. It generates the next key-stream block by encrypting successive values named as
”counter”. This counter can be any purpose or function which generates a sequence that
is guaranteed not to call for a long time, although an actual increment-by-one counter is
the simplest or easiest and most popular or famous.In the CTR mode, we
start off with a random seed, s, and compute pad vectors according to the formula:
Vi = EK(s + i − 1)
where EK denotes the block encryption algorithm using key K, Vi
is a pad vector, and i is the vector’s offset starting from 1.
Now that the vectors have been generated, encryption
similar to the mode can proceed using the following formula:
Ci = Vi ⊕ Bi
Decryption is carried out in a similar way
Bi = Vi ⊕ Ci.

## About The Code

### Serpent Code


### Serpent CTR Code


## How To Run
### Using Terminal/Command Line
#### System Requirement
1. Python 3.x or higher.

#### Run Command
To run the code you need to decide first whick operation you want to do, it's either encryption or decryption, for each operation you need to use specific oprions in the command.

The code provide also using ctr mode to encrypt and decrypt, so will split it into two type here.

#### Run Command Without CTR
##### Encryption
You need only two options here:
* ``` -e ``` for encryption mode
* ``` -p ``` for the plain text and must be string of bits that has length dividable by 128

Sample Command From root folder

``` python serpent\test_serpent.py -e -p 10100000101101111101010101101011010101010100000101111110101101010101110011011101010101010101110101010101010101011101011111110010 ``` 

The output will have a key and cipher text, you can use them to decrypt later, here is a sample

```
The Plain text is:  10100000101101111101010101101011010101010100000101111110101101010101110011011101010101010101110101010101010101011101011111110010
The Cipher text is:  11101001000110111101000101011110111000111010110011001000010001111101011110010000010110011010100101111101001110100100110111001110
The key is:  ffa998964f6d59f8b30325c453e3a11b0b685d7e6e8e9eaeaeaeaeaeaeaea 
```

##### Decryption 
For decryption you need to provide 3 options:
* ``` -d ``` for decryption mode
* ``` -c ``` for the cipher text which is output from encryption method
* ``` -k ``` for the key that algorithm will use to decrypt which is output from encryption method

Sample Command From root folder
```
python serpent\test_serpent.py -d -c 11101001000110111101000101011110111000111010110011001000010001111101011110010000010110011010100101111101001110100100110111001110 -k ffa998964f6d59f8b30325c453e3a11b0b685d7e6e8e9eaeaeaeaeaeaeaea
```

As output you will get the original text, here is a sample

```
The Cipher text is:  11101001000110111101000101011110111000111010110011001000010001111101011110010000010110011010100101111101001110100100110111001110
The Plain text is:  10100000101101111101010101101011010101010100000101111110101101010101110011011101010101010101110101010101010101011101011111110010
```

#### Run Command With CTR
##### Encryption
Same as the prevois one, just the output will have extra output.
* ``` -e ``` for encryption mode
* ``` -p ``` for the plain text and must be string of bits that has length dividable by 128

Sample Command From root folder

``` python serpent\test_serpent_ctr.py -e -p 10100000101101111101010101101011010101010100000101111110101101010101110011011101010101010101110101010101010101011101011111110010 ``` 

The output now have Base IV, here is a sample

```
The Plain text is:  10100000101101111101010101101011010101010100000101111110101101010101110011011101010101010101110101010101010101011101011111110010
The Cipher text is:  00000100111111001111000100100101000001000011101110011010001011000101110100101010011010101101101011111011000100100000001110010111
The key is:  053227176d337d2e686da46737d79dfa975435df8bbad44533529ead9c7c5
The Base IV is :  0111011111001011111011011001110100111101101010110010010011001110
```

##### Decryption 
For decryption you need to provide the prevois 3 options and Base IV:
* ``` -d ``` for decryption mode
* ``` -c ``` for the cipher text which is output from encryption method
* ``` -k ``` for the key that algorithm will use to decrypt which is output from encryption method
* ``` -i ``` for the Base IV which is output from encryption method

Sample Command From root folder
```
python serpent\test_serpent.py -d -c 00000100111111001111000100100101000001000011101110011010001011000101110100101010011010101101101011111011000100100000001110010111 -k 053227176d337d2e686da46737d79dfa975435df8bbad44533529ead9c7c5 -i 0111011111001011111011011001110100111101101010110010010011001110
```

As output you will get the original text, here is a sample

```
The Cipher text is:  11101001000110111101000101011110111000111010110011001000010001111101011110010000010110011010100101111101001110100100110111001110
The Plain text is:  10100000101101111101010101101011010101010100000101111110101101010101110011011101010101010101110101010101010101011101011111110010
```


### Using Docker
- Will come soon.
