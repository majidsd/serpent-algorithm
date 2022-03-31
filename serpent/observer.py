import helper as help_functions

class Observer:
    """An object of this class can selectively display the values of the
    variables you want to observe while the program is running. There are
    tags that you can switch on or off. You sprinkle show() statements
    throughout the program to show the value of a variable at a particular
    point: show() will display the relevant variable only if the
    corresponding tag is currently on. The special tag "ALL" forces all
    show() statements to display their variable."""

    typesOfVariable = {
        "tu": "unknown", "tb": "bitstring", "tlb": "list of bitstrings",}
    def __init__(self, tags=[]):
        self.tags = {}
        for tag in tags:
            self.tags[tag] = 1


    def addTag(self, *tags):
        """Add the supplied tag(s) to those that are currently active,
        i.e. those that, if a corresponding "show()" is executed, will
        print something."""

        for t in tags:
            self.tags[t] = 1

    def removeTag(self, *tags):
        """Remove the supplied tag(s) from those currently active."""
        for t in tags:
            if t in self.tags.keys():
                del self.tags[t]

    def show(self, tag, variable, label=None, type="tb"):
        """Conditionally print a message with the current value of
        'variable'. The message will only be printed if the supplied 'tag'
        is among the active ones (or if the 'ALL' tag is active). The
        'label', if not null, is printed before the value of the
        'variable'; if it is null, it is substituted with the 'tag'. The
        'type' of the 'variable' (giving us a clue on how to print it) must
        be one of Observer.typesOfVariable."""

        if label == None: #O.show("BHati", BHati, "(i=%2d) BHati" % i)
            label = tag
        if "ALL" in self.tags.keys() or tag in self.tags.keys():
            if type == "tu":
                output = 'variable'
            elif type == "tb":
                output = help_functions.bitstring2hexstring(variable)
            elif type == "tlb":
                output = ""
                for item in variable:
                    output = output + " %s" % help_functions.bitstring2hexstring(item)
                output = "[" + output[1:] + "]"
            else:
                raise ValueError( "the %d is not in the supportted types." % type)

            print (label)
            if output:
                print ("=", output)
            else:
                print