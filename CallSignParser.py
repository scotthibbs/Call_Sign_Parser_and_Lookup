import tkinter as tk
import re


""" 
Python Call Sign Parser with Interface
Copyright (c) 2022 by Scott Anthony Hibbs KD4SIR 
Released under a GPLv3 License. 
If you do use or modify this software, 
I'd really love to hear about it at scott hibbs at gmail dot com.

Type a call sign in the input box and get the result
from the cty.dat file. This can be updated at  
https://www.country-files.com/category/big-cty/
maintained with my thanks by Jim Reisert AD1C
- Scott KD4SIR
"""

# Top level window
frame = tk.Tk()
frame.title("Call Sign Parser by Scott Hibbs KD4SIR")
frame.geometry('500x250')


class CallSignParser:
    """ Takes a call sign and returns prefix, sepdig, suffix, country and valid prefix check (true or false)"""

    def __init__(self):
        pass

    @staticmethod
    def lastofthelist(alistinp):
        """ Removes the last character and returns the new last character """
        new_lst = alistinp[::-1]
        onlythisone = [new_lst[0]]
        return onlythisone

    @staticmethod
    def reversethis(sdrawkcab):
        """ Reverses the order of a list. """
        new2_lst = sdrawkcab[::-1]
        return new2_lst

    @staticmethod
    def justthefix(tryfix):
        """ this will return the prefix, seperator and suffix in string format if given a call sign"""
        # The call sign (tryfix) is reversed to find the suffix.
        prefsuf = CallSignParser.reversethis(tryfix)
        # create lists for the suffix and prefix.
        suffix = []
        prefix = []
        # we need the list of numbers to find the seperator. At first the seperator is part of the prefix.
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        # counters are used to keep track of where we are at in the process.
        counter3 = 0  # separator counter.
        counter4 = 0  # number counter in case of slash.
        # how many numbers are there in this thing?
        questdig = sum(c1.isdigit() for c1 in tryfix)
        #  questdig is used later in case the call sign only has one digit.
        # call signs that start with numbers are cool
        str1letter = tryfix[0]
        if str1letter.isdigit():
            questdig = questdig - 1
        # We have to check for slashes either way first.
        if "/" in tryfix or "\\" in tryfix:
            for item1 in prefsuf:
                # print("item1 is " + str(item1))
                if item1 == "/" or item1 == "\\":
                    # print("counter4 is " + str(counter4))
                    suffix.pop(counter4)
                    continue
                else:
                    counter4 -= 1  # increment backwards to give amount to erase with slash
                if item1.isdigit():
                    if questdig == 1:
                        counter3 += 1  # seperator trigger (we add suffixes then prefixes)
                    else:
                        questdig -= 1  # reduce the count of the numbers
                if counter3 < 1:
                    suffix.append(item1)
                else:
                    prefix.append(item1)
        else:
            # no slashes so going backwards same as above, we append the suffix until a number then the rest is prefix.
            for item in prefsuf:
                if item in numbers:
                    counter3 += 1
                if counter3 < 1:
                    suffix.append(item)
                else:
                    prefix.append(item)
        # now we seperate the separator from the prefix.
        seperatdig = [prefix[0]]
        strsepdig = str(seperatdig)
        # set the prefix to read forward and remove the separator.
        prefix = CallSignParser.reversethis(prefix)
        del prefix[-1]
        # set the suffix to read forward.
        suffix = CallSignParser.reversethis(suffix)
        # Now we want to put the list values together in one value and return them as strings.
        strsepdig = strsepdig.join(seperatdig)
        strprefix = ""
        strprefix = strprefix.join(prefix)
        strsuffix = ""
        strsuffix = strsuffix.join(suffix)
        return strprefix, strsepdig, strsuffix

    @staticmethod
    def ctyfileread(checkprefix, sepdig):
        """ reads the cty.dat file and returns the country """
        dxname = ""
        dxprefix = list()
        dictdx = {dxname: dxprefix}
        thisnow = ""
        try:
            cty_file = open("cty.dat", "r")  # read cty.dat
            while 1:
                lnx = cty_file.readline()  # read a line
                if not lnx:
                    break
                if re.match(r'\w', lnx):
                    nameline = 1
                else:
                    nameline = 0
                if nameline == 1:
                    thisnow = lnx.split(':')[0]
                    #  print(thisnow)
                    dictdx[thisnow] = list()
                else:
                    # remove simicolon, spaces, new lines, brackets with numbers, and parentheses with numbers
                    datapref = lnx.split(',')
                    datapref2 = [re.sub(';', '', datapref) for datapref in datapref]
                    datapref3 = [re.sub(' ', '', datapref2) for datapref2 in datapref2]
                    datapref4 = [re.sub('\n', '', datapref3) for datapref3 in datapref3]
                    datapref5 = [re.sub(r"\[\d*?]", '', datapref4) for datapref4 in datapref4]
                    datapref6 = [re.sub(r"\(\d*?\)", '', datapref5) for datapref5 in datapref5]
                    dictdx[thisnow].append(datapref6)
        finally:
            pass
        # needs to be upper to match the cty.dat file
        final = checkprefix.upper()
        # Need exceptions to the list such as single letter country calls.
        try:
            final1 = final[0]
            singles = ['B', 'F', 'G', 'I', 'K', 'M', 'N', 'R', 'W']
            if final1 in singles:
                final = final[0]
            # Exception to the A calls
            if final1 == "A":
                try:
                    final2 = final[1]
                    if final2.isdigit():
                        final = final1 + final2
                    if final2 == "":
                        final = final1 + sepdig
                    else:
                        final = final1 + final2
                except IndexError:
                    pass
        except IndexError:
            pass
        # Let's find this thing in the dictionary we created from cty.dat
        country = [key for key, val in dictdx.items() if any(final in s for s in val)]
        if len(country) == 0:
            finalexept = final + sepdig
            final = finalexept
            country = [key for key, val in dictdx.items() if any(final in s for s in val)]
            if len(country) == 0:
                country = "unassigned?"
        country1 = str(country)
        country2 = re.sub(r"[\[\]]", '', country1)
        country3 = country2.replace("'", "")
        return country3

    @staticmethod
    def validprefix(country5):
        """ Checks the result of ctyfileread() to see if the country is valid true or false."""
        if country5 == "unassigned?" or country5 == "":
            return False
        else:
            return True

    @staticmethod
    def callsignresults(tryfix):
        """ Returns everything this class offers if given a call sign."""
        strprefix1, strsepdig1, strsuffix1 = CallSignParser.justthefix(tryfix)
        country4 = CallSignParser.ctyfileread(strprefix1, strsepdig1)
        valid1 = CallSignParser.validprefix(country4)
        # returns prefix, seperator, suffix, country name and prefix true/false
        return strprefix1, strsepdig1, strsuffix1, country4, valid1


def printinput1():
    # get inputent
    inp = inputent.get()
    if len(inp) == 0:
        return
    # initializing list
    listinp = list(inp)
    # printing the input list
    lblrepeat.config(text="\n The original input is: " + str(listinp))
    # try my suffix routine
    strprefix, strsepdig, strsuffix = CallSignParser.justthefix(listinp)
    # Now let's find out where that call is from
    ourcountry = CallSignParser.ctyfileread(strprefix, strsepdig)
    lblreturn.config(text="This is from: " + str(ourcountry))
    # configure the labels.
    lblsuffix.config(text="The suffix is: " + strsuffix)
    lblprefix.config(text="The prefix is: " + strprefix)
    lblseperator.config(text="The separator is: " + strsepdig)


# Main Program
lbltitle = tk.Label(frame, text="\nCall Sign Look Up")
lbltitle.pack()
# Entry Widget creation
inputent = tk.Entry(frame, width=30, justify="center")
inputent.pack()
# Button Creation
printButton = tk.Button(frame, text="Search", command=printinput1)
printButton.pack()
# Label Creation
lblrepeat = tk.Label(frame, text="")
lblrepeat.pack()
lblprefix = tk.Label(frame, text="The prefix:")
lblprefix.pack()
lblseperator = tk.Label(frame, text="The seperator:")
lblseperator.pack()
lblsuffix = tk.Label(frame, text="The suffix:")
lblsuffix.pack()
lblreturn = tk.Label(frame, text="Results:")
lblreturn.pack()

a, b, c, d, e, = CallSignParser.callsignresults("KD4SIR")
print(a, b, c, d, e)

# Bindings
frame.bind('<Return>', (lambda event: printinput1()))

frame.mainloop()
