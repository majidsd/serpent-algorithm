import sys
import getopt

import helper as help_functions
import serpent as normal_serpent
import observer as observer


def main():
    observer_object = observer.Observer(["plainText", "userKey", "cipherText"])
    opts, args = getopt.getopt(sys.argv[1:], "edhbt:k:p:c:i:")
    
    if args:
        help_functions.helpExit("Sorry, can't make sense of this: '%s'" % args)

    options = {}
    for opt, arg in opts:
        if opt == "-t":
            observer_object.addTag(arg)
        else:
            if opt in options.keys():
                help_functions.helpExit("Multiple occurrences of " + opt)
            else:
                options[str.strip(opt)] = str.strip(arg)
    
    # Not more than one mode
    mode = None
    for key in options.keys():
        if key in ["-e", "-d", "-h"]:
            if mode:
                help_functions.helpExit("You can only specify one mode")
            else:
                mode = key

    if not mode:
        help_functions.helpExit("No mode specified")
   
    # Put plainText, userKey, cipherText in bitstring format.
    plainText =  cipherText = userKey = None
    
    if  ('-p') in str(options):
        plainText = options["-p"]
        
    if ('-c') in str(options):
        cipherText = options["-c"]
        
    if mode == "-e":
        if not plainText:
            help_functions.helpExit("-p (plaintext) is required when doing -e (encrypt)")
    if mode == "-d":
        if not cipherText:
            help_functions.helpExit("-c (ciphertext) is required when doing -d (decrypt)")
             
    if mode == "-e":
        userKey = help_functions.key_gen()
        print('************************** Starting encryption **************************')
        print('The Plain text is: ', plainText)
        print("The Cipher text is: ", normal_serpent.encrypt(plainText, help_functions.convertToBitstring(userKey, 256)))
        print("The key is: ", userKey)
    elif mode == "-d":
        userKey = options["-k"]
        if not userKey:
            help_functions.helpExit('-k (key) required with -d (decrypt)')
     
        print('************************** Starting decryption **************************')
        print('The Cipher text is: ', cipherText)
        print('The Plain text is: ', normal_serpent.decrypt(cipherText, help_functions.convertToBitstring(userKey, 256)))
    else:
        help_functions.helpExit()

if __name__ == "__main__":
    main()