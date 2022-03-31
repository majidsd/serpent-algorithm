import helper as help_functions
import sys
import getopt
import serpent as normal_serpent
import observer as observer

O = observer.Observer(["plainText", "userKey", "cipherText"])

def main():
    optList, rest = getopt.getopt(sys.argv[1:], "edhbt:k:p:c:i:")
    
    if rest:
        help_functions.helpExit("Sorry, can't make sense of this: '%s'" % rest)

    # Transform the list of options into a more comfortable
    # dictionary. This only works with non-repeated options, though, so
    # tags (which are repeated) must be dealt with separately.
    options = {}
    
    for key, value in optList:
        if key == "-t":
            O.addTag(value)
        else:
            if key in options.keys():
                help_functions.helpExit("Multiple occurrences of " + key)
            else:
                options[str.strip(key)] = str.strip(value)
    
    # Not more than one mode
    mode = None
    
    for k in options.keys():
        if k in ["-e", "-d", "-h"]:
            if mode:
                help_functions.helpExit("you can only specify one mode")
            else:
                mode = k

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
            
    
    # Perform the action specified by the mode
    # NOTE that the observer will automatically print the basic stuff such
    # as plainText, userKey and cipherText (in the right format too), so we
    # only need to perform the action, without adding any extra print
    # statements here.
    if mode == "-e":
        userKey = help_functions.key_gen()
        iVBase = help_functions.random_iv(64)
        print('Plain text=', plainText)
        print("The Cipher text is: ", normal_serpent.encrypt_ctr(plainText, help_functions.convertToBitstring(userKey, 256), iVBase, 2))
        print("The key is: ", userKey)
        print("The Base IV is : ", iVBase)

    elif mode == "-d":
        userKey = options["-k"]
        iv = options["-i"]

        if not userKey:
            help_functions.helpExit("-k (key) required with -d (decrypt)")
                
        print('Cipher text: ', cipherText)
        print("The Plain text is: ", normal_serpent.decrypt_ctr(cipherText, help_functions.convertToBitstring(userKey, 256), iv, 2))

    else:
        help_functions.helpExit()

if __name__ == "__main__":
    main()