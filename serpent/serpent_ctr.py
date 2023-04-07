import helper as helper_functions
import serpent as normal_serpent

import multiprocessing

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

def do_bulk_encrypt(sub_blocks, nonce, key):
    encrypted_sub_blocks = []

    for plaintext_block in sub_blocks:
        block = helper_functions.binaryXor(plaintext_block, normal_serpent.encrypt(nonce, key))
        encrypted_sub_blocks.append(block)
        nonce = inc_bytes((nonce))
    return ''.join(encrypted_sub_blocks)

def do_bulk_decrypt(sub_blocks, nonce, key):
    decrypted_sub_blocks = []

    for ciphertext_block in sub_blocks:
        block = helper_functions.binaryXor(normal_serpent.encrypt(nonce, key), ciphertext_block)
        decrypted_sub_blocks.append(block)
        nonce = inc_bytes((nonce))
    return ''.join(decrypted_sub_blocks)

def encrypt_ctr(plaintext, user_key, iv_base, number_of_processes):
    nonce_base = iv_base
    splited_blocks = split_blocks(plaintext, require_padding=False)

    data_size = len(splited_blocks)
    chunk_data = int(data_size/number_of_processes)

    if chunk_data == 0:
        chunk_data = 1

    arguments = []
    for i in range(0, data_size, chunk_data):
        arguments.append((splited_blocks[i: i + chunk_data], nonce_base + helper_functions.convert_decimel_to_binary64(i), user_key))

    with multiprocessing.Pool() as pool:
        ciphered_blocks = pool.starmap(do_bulk_encrypt, arguments)

    return ''.join(ciphered_blocks)

def decrypt_ctr(cipherText, user_key, iv_base, number_of_processes):
    nonce_base = iv_base
    splited_blocks = split_blocks(cipherText, require_padding=False)
    
    data_size = len(splited_blocks)
    chunk_data = int(data_size/number_of_processes)

    if chunk_data == 0:
        chunk_data = 1

    arguments = []
    for i in range(0, data_size, chunk_data):
        arguments.append((splited_blocks[i: i + chunk_data], nonce_base + helper_functions.convert_decimel_to_binary64(i), user_key))

    with multiprocessing.Pool() as pool:
        plain_blocks = pool.starmap(do_bulk_decrypt, arguments)

    return ''.join(plain_blocks)
