
import helper as helper_functions
import serpent as normal_serpent
import serpent_ctr as ctr_serpent

import time as time

def make_inupt_for_serpent_32_hexa(how_many):
    assert how_many > 0
    single_item = '123456789abcdef123456789abcdef12'
    full_text = []
    for i in range(how_many):
        full_text.append(single_item)
    return ''.join(full_text)

def make_inupt_for_serpent_128_bits(how_many):
    assert how_many > 0
    single_item = '11010110110101010101001110100011011011110101001001101110100110001111000010010001011011100000110001011110100011000101011111011000'
    full_text = []
    for i in range(how_many):
        full_text.append(single_item)
    return ''.join(full_text)

def normal_serpant_performance(data_size):
    full_cipher_text = []
    full_plain_text = []

    user_key = helper_functions.convertToBitstring('fff66963ceea4d72f552fec4cb3ae08d9faa3bc4df81309b8bcff9d320e1651', 256)
    
    # Data to do test
    text_serpent = make_inupt_for_serpent_128_bits(data_size)
    
    # Encrypt Test
    t0 = time.time()
    blocks = ctr_serpent.split_blocks(text_serpent)
    for block in blocks:
        cipher_text = normal_serpent.encrypt(block, user_key)
        full_cipher_text.append(cipher_text)
    t1 = time.time()
    print('Total time to encrypt ', data_size, ' blocks is: ', t1-t0)

    # Decrypt Test
    t0 = time.time()
    blocks = ctr_serpent.split_blocks(text_serpent)
    for block in blocks:
        plain_text = normal_serpent.decrypt(block, user_key)
        full_plain_text.append(plain_text)
    t1 = time.time()
    print('Total time to decrypt ', data_size, ' blocks is: ', t1-t0)

def ctr_serpant_performance(data_size, number_of_processes):
    user_key = helper_functions.convertToBitstring('fff66963ceea4d72f552fec4cb3ae08d9faa3bc4df81309b8bcff9d320e1651', 256)
    iv_base = helper_functions.random_iv(64)

    # Data to test encrypt
    text_serpent_ctr = make_inupt_for_serpent_128_bits(data_size)
    
    # Encrypt Test
    t0 = time.time()
    ctr_serpent.encrypt_ctr(text_serpent_ctr, user_key, iv_base, number_of_processes)
    t1 = time.time()
    print('Total time to encrypt (CTR) ', data_size, ' blocks is: ', t1-t0, ' using ', number_of_processes, ' threads')

    # Decrypt Test
    t0 = time.time()
    ctr_serpent.decrypt_ctr(text_serpent_ctr, user_key, iv_base, number_of_processes)
    t1 = time.time()
    print('Total time to decrypt (CTR) ', data_size, ' blocks is: ', t1-t0, ' using ', number_of_processes, ' threads')

if __name__ == "__main__":
    blocks = [64, 128, 256, 512, 1024]
    
    for i in range(2):
        print('Round: ', i)
        for j in blocks:
            normal_serpant_performance(j)
            time.sleep(3)

    for i in range(2):
        print('Round: ', i)
        # 2 threads
        for j in blocks:
            ctr_serpant_performance(j, 2)
            time.sleep(3)

        # 4 threads
        for j in blocks:
            ctr_serpant_performance(j, 4)
            time.sleep(3)

        # 8 threads
        for j in blocks:
            ctr_serpant_performance(j, 8)
            time.sleep(3)