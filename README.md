## About Serpent Algorithm

## About The Code


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
