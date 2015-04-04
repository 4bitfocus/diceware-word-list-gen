#!/usr/bin/env python

"""Diceware dictionary generator

This script generates a diceware.txt file in the current directory for use
with the Diceware method of password selection. Basic instructions are in
the file; full instructions can be found here:
http://world.std.com/~reinhold/diceware.html
"""

__author__ = 'Kevin Douglas'
__email__ = 'douglk@gmail.com'
__version__ = 1.0

import os
import sys
import random
import math
import argparse

def gen_word_list(file_name, min_word_length = 3, max_word_length = 7):
    """Generate a word list from a given dictionary file filtering based
    on word length."""
    lst = [ ]
    with open(file_name) as fp:
        for line in fp:
            line = line.strip()
            length = len(line)
            if length < min_word_length or length > max_word_length: continue
            if line[0].isupper(): continue
            lst.append(line)
    return lst

def gen_char_table():
    """Generate the special character table for optional/additional security."""
    chars = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
              '!', '@', '#', '$', '%', '~', '^', '&', '*', '(',
              ')', '-', '=', '_', '+', '[', ']', '{', '}', ':',
              ';', '<', '>', '\'', '"', '?', '/', '\\' ]
    tbl = { }
    picked = [ ]
    for r in range(1, 7):
        tbl[r] = [ ]
        for c in range(1, 7):
            while True:
                a = random.choice(chars)
                if a in picked: continue
                picked.append(a)
                tbl[r].append(a)
                break
    return tbl

def gen_dice_map(words):
    """Creates a dictionary of dice keys to words."""
    dct = { }
    # Make sure the word list can support 5 picks from 6 sided dice
    if len(words) < math.pow(6, 5):
        raise RuntimeError('word list too short')
    for d1 in range(1, 7):
        for d2 in range(1, 7):
            for d3 in range(1, 7):
                for d4 in range(1, 7):
                    for d5 in range(1, 7):
                        while True:
                            w = random.choice(words)
                            if w in dct.values(): continue
                            if len(w) == 1:
                                print w
                            key = "{d1}{d2}{d3}{d4}{d5}".format(**locals())
                            dct[key] = w
                            break
    return dct

def main():
    default_dict = '/usr/share/dict/words'
    parser = argparse.ArgumentParser(description="generates a diceware.txt dictionary file")
    parser.add_argument('dict_names', help='file containing a list of words (default: {0})'.format(default_dict), \
            metavar='dict', nargs='*', default=[default_dict])
    parser.add_argument('--output', '-o', help='output file name (default: %(default)s)', \
            metavar='file', default='diceware.txt')
    args = parser.parse_args()
    words = [ ]
    for file_name in args.dict_names:
        if not os.path.exists(file_name):
            print "file not found: {0}".format(file_name)
            continue
        words.extend(gen_word_list(file_name))
    print "found {0} words".format(len(words))
    dice_words = gen_dice_map(words)
    with open(args.output, 'w') as fp:
        fp.write("Roll five dice for each word in your passphrase. Match up\n")
        fp.write("the 5 digits (e.g. 35126) in the list below.\n\n")
        for k,v in sorted(dice_words.iteritems()):
            fp.write("{0} {1}\n".format(k, v))
        fp.write("\nSpecial Character Table\n\n")
        fp.write("Roll one die to choose a word in your passphrase, roll\n")
        fp.write("again to choose a letter in that word. Roll a third and\n")
        fp.write("fourth time to pick the added character from the\n")
        fp.write("following table:\n\n")
        fp.write("  1 2 3 4 5 6\n")
        for row,row_list in gen_char_table().iteritems():
            fp.write("{0} ".format(row))
            for i, char in enumerate(row_list):
                fp.write("{0}".format(char))
                if i != len(row_list) - 1:
                    fp.write(" ")
            fp.write("\n")
        fp.write("\nFull reference here: http://world.std.com/~reinhold/diceware.html\n")
    print "created file '{0}'".format(args.output)
    return 0

if __name__ == '__main__':
    sys.exit(main())
