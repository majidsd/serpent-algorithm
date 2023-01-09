import helper as helper_functions
import serpent as normal_serpent

import threading
import concurrent.futures

class serpant_ctr (threading.Thread):
    def __init__(self, thread_id, name, sub_blocks, nonce, key):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.sub_blocks = sub_blocks
        self.nonce = nonce
        self.key = key
    
    def run(self):
        print("Starting "+ self.name)
        encrypted_sub_blocks = []
        for plaintext_block in self.sub_blocks:
            block = helper_functions.binaryXor(plaintext_block, normal_serpent.encrypt((self.nonce), self.key))
            encrypted_sub_blocks.append(block)
            self.nonce = inc_bytes((self.nonce))
        print("End "+ self.name)
        return ''.join(encrypted_sub_blocks)

def inc_bytes(a):
    """ Returns a new byte array with the value increment by 1 """
    b = '1'
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
    
def split_blocks(message, block_size=128, require_padding=False):
    assert len(message) % block_size == 0 or not require_padding
    return [message[i:i+128] for i in range(0, len(message), block_size)]

def do_bulk_encrypt(name, sub_blocks, nonce, key):
    encrypted_sub_blocks = []
        
    for plaintext_block in sub_blocks:
        block = helper_functions.binaryXor(plaintext_block, normal_serpent.encrypt(nonce, key))
        encrypted_sub_blocks.append(block)
        nonce = inc_bytes((nonce))
    return ''.join(encrypted_sub_blocks)

def do_bulk_decrypt(name, sub_blocks, nonce, key):
    decrypted_sub_blocks = []

    for ciphertext_block in sub_blocks:
        block = helper_functions.binaryXor(normal_serpent.encrypt(nonce, key), ciphertext_block)
        decrypted_sub_blocks.append(block)
        nonce = inc_bytes((nonce))
    return ''.join(decrypted_sub_blocks)

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
            future = executor.submit(lambda p: do_bulk_encrypt(*p), args)
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
            future = executor.submit(lambda p: do_bulk_decrypt(*p), args)
            futures_list.append(future)
            count += count
        
        for item in futures_list:
            plain_text += item.result()
    return plain_text
