import helper as helper_functions
import serpent as normal_serpent

import threading
import concurrent.futures


class EncryptCTR (threading.Thread):
    def __init__(self, threadID, name, subBlocks, nonce, key):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.subBlocks = subBlocks
        self.nonce = nonce
        self.key = key
    
    def run(self):
        print("Starting "+ self.name)
        encryptedSubBlocks = []
        
        for plaintext_block in self.subBlocks:
            block = helper_functions.binaryXor(plaintext_block, normal_serpent.encrypt((self.nonce), self.key))
            encryptedSubBlocks.append(block)
            self.nonce = inc_bytes((self.nonce))
        
        print("End "+ self.name)
        return ''.join(encryptedSubBlocks)


def inc_bytes(a):
    """ Returns a new byte array with the value increment by 1 """
    b='1'
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    # Initialize the result
    result = ''
    # Initialize the carry
    carry = 0
    # Traverse the string
    for i in range(max_len - 1, -1, -1):
        r = carry
        r += 1 if a[i] == '1' else 0
        r += 1 if b[i] == '1' else 0
        result = ('1' if r % 2 == 1 else '0') + result
        # Compute the carry.
        carry = 0 if r < 2 else 1
    if carry != 0:
        result = '1' + result
    return(result.zfill(max_len))
    

def split_blocks(message, block_size=128, require_padding=True):
    assert len(message) % block_size == 0 or not require_padding
    return [message[i:i+128] for i in range(0, len(message), block_size)]


def DoBulkEncrypt(name, subBlocks, nonce, key):
    #print("Starting "+ name)
    encryptedSubBlocks = []
    print(nonce,subBlocks[0])
        
    for plaintext_block in subBlocks:
        block = helper_functions.binaryXor(plaintext_block, normal_serpent.encrypt((nonce), key))
        encryptedSubBlocks.append(block)
        nonce = inc_bytes((nonce))
        
    #print("End "+ name)
    return ''.join(encryptedSubBlocks)


def DoBulkDecrypt(name, subBlocks, nonce, key):
    #print("Starting "+ name)
    encryptedSubBlocks = []
    print(nonce,subBlocks[0])
    for ciphertext_block in subBlocks:
        block = helper_functions.binaryXor(ciphertext_block, normal_serpent.decrypt((nonce), key))
        encryptedSubBlocks.append(block)
        nonce = inc_bytes((nonce))
        
    #print("End "+ name)
    return ''.join(encryptedSubBlocks)


def encrypt_ctr(plaintext, userKey, iv_base, number_of_thread):

    cipher_text = '' 
    nonce_base = iv_base

    splited_blocks = split_blocks(plaintext, require_padding=False)
    data_size = len(splited_blocks)
    
    chunk_data = int(data_size/number_of_thread)


    if chunk_data == 0:
        chunk_data = 1

    count = 1

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures_list = []
        for i in range(0, data_size, chunk_data):
            args = ["Task " + str(count), splited_blocks[i: i + chunk_data], nonce_base + helper_functions.convert_decimel_to_binary64(i), userKey]
            future = executor.submit(lambda p: DoBulkDecrypt(*p), args)
            futures_list.append(future)
            count += count
        
        for item in futures_list:
            cipher_text += item.result()

    return cipher_text


def decrypt_ctr(cipherText, userKey, iv_base, number_of_thread):

    plain_text = '' 
    nonce_base = iv_base

    splited_blocks = split_blocks(cipherText, require_padding=False)
    data_size = len(splited_blocks)
    
    chunk_data = int(data_size/number_of_thread)

    if chunk_data == 0:
        chunk_data = 1

    count = 1

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures_list = []
        for i in range(0, data_size, chunk_data):
            args = ["Task " + str(count), splited_blocks[i: i + chunk_data], nonce_base + helper_functions.convert_decimel_to_binary64(i), userKey]
            future = executor.submit(lambda p: DoBulkEncrypt(*p), args)
            futures_list.append(future)
            count += count
        
        for item in futures_list:
            plain_text += item.result()

    return plain_text
