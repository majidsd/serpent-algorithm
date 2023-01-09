import sys
import getopt

import helper as help_functions
import serpent_ctr as ctr_serpent
import observer as observer

def main():
    number_of_thread = 2
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
            
    
    # Perform the action specified by the mode
    # NOTE that the observer will automatically print the basic stuff such
    # as plainText, userKey and cipherText (in the right format too), so we
    # only need to perform the action, without adding any extra print
    # statements here.
    if mode == "-e":
        if ('-k') in str(options):
            userKey = options['-k']
        else:
            userKey = help_functions.key_gen()
            
        iVBase = help_functions.random_iv(64)
        print('The Plain text is: ', plainText)
        print('The Cipher text is: ', ctr_serpent.encrypt_ctr(plainText, help_functions.convertToBitstring(userKey, 256), iVBase, number_of_thread))
        print('The key is: ', userKey)
        print('The Base IV is : ', iVBase)

    elif mode == "-d":
        userKey = options["-k"]
        iv = options["-i"]

        if not userKey or not iv:
            help_functions.helpExit("-k (key) and -i (iv) required with -d (decrypt)")
                
        print('The Cipher text: ', cipherText)
        print("The Plain text is: ", ctr_serpent.decrypt_ctr(cipherText, help_functions.convertToBitstring(userKey, 256), iv, number_of_thread))

    else:
        help_functions.helpExit()

if __name__ == "__main__":
    main()