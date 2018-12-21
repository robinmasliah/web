# Written with <3 by Julien Romero

import hashlib
from sys import argv
import sys

if (sys.version_info > (3, 0)):
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    from urllib2 import urlopen
    from urllib import urlencode
import pandas as pd


class Crack:
    """Crack The general method used to crack the passwords"""

    leet_dict = {'a': ['@'], }

    def __init__(self, filename, name):
        """__init__
        Initialize the cracking session
        :param filename: The file with the encrypted passwords
        :param name: Your name
        :return: Nothing
        """
        self.name = name.lower()
        self.passwords = get_passwords(filename)

    def check_password(self, password):
        """check_password
        Checks if the password is correct
        !! This method should not be modified !!
        :param password: A string representing the password
        :return: Whether the password is correct or not
        """
        password = str(password)
        cond = False
        if (sys.version_info > (3, 0)):
            cond = hashlib.md5(bytes(password, "utf-8")).hexdigest() in \
                   self.passwords
        else:
            cond = hashlib.md5(bytearray(password)).hexdigest() in \
                   self.passwords
        if cond:
            args = {"name": self.name,
                    "password": password}
            args = urlencode(args, "utf-8")
            page = urlopen('https://julienromero.com/ATHENS/' +
                           'submit?' + args)
            if b'True' in page.read():
                print("You found the password: " + password)
                return True
        return False

    def crack(self, method):
        if method == 'TOP':
            self.crack_top_password
        elif method == 'COMMON':
            self.crack_most_common_words()
        elif method == 'DIGITS':
            self.crack_10_digits_range()
        elif method == 'LETTERS':
            self.crack_5_letters()
        elif method == 'DICE':
            self.crack_diceware_passwords()
        elif method == 'LEET':
            self.crack_leet_words()
        elif method == 'CITIES':
            self.crack_cities()

    def crack_top_password(self):
        with open(
                '/home/cyril/projects/INF344-Donnees_du_web/probable-v2-top12000.txt',
                "r") as f:
            for line in f:
                self.check_password(line.strip())

    def crack_most_common_words(self):
        with open('/home/cyril/projects/INF344-Donnees_du_web/wiki-100k.txt',
                  "r") as f:
            for line in f:
                self.check_password(line.strip().lower())

    def crack_10_digits_homemade(self):
        for password in create_passwords(10):
            self.check_password(password)

    def crack_5_letters(self):
        count = 0
        for password in create_passwords_abc(5):
            count += 1
            if count % 100000 == 0:
                print('testing ' + password)

            self.check_password(password)

    def crack_10_digits_range(self):
        count = 0
        for password in range(3000000000, 4000000000):
            count += 1
            if count % 100000000 == 0:
                print('testing ' + str(password))
            self.check_password(str(password))

    def crack_diceware_passwords(self):
        count = 0
        words = []
        with open(
                '/home/cyril/projects/INF344-Donnees_du_web/google-10000-english-usa.txt',
                "r") as f:
            for line in f:
                words += [line.strip().lower()]

        for word1 in words:
            for word2 in words:
                password = word1 + '-' + word2
                count += 1
                if count % 100000 == 0:
                    print('testing ' + password)
                self.check_password(password)

    def crack_leet_words(self):
        count = 0
        with open('/home/cyril/projects/INF344-Donnees_du_web/wiki-100k.txt',
                  "r") as f:
            for line in f:
                if line[0] == '#':
                    continue
                for leet_word in get_leet_words(line.strip().lower()):
                    count += 1
                    if count % 100000 == 0:
                        print('testing ' + leet_word)
                    self.check_password(leet_word)

    def crack_cities(self):
        df = pd.read_csv('villes_france.csv', header=None)
        count = 0
        for town in df[5]:
            if count % 1000 == 0:
                print('testing ' + town)
            self.check_password(town.lower)


def create_passwords(nb_digits):
    for i in range(1, nb_digits + 1):
        for password in create_passwords_fixed_size(i):
            yield password


def create_passwords_fixed_size(nb_digits):
    for i in range(10):
        if nb_digits > 1:
            for password in create_passwords_fixed_size(nb_digits - 1):
                yield password + str(i)
        else:
            yield str(i)


def create_passwords_abc(nb_digits):
    for i in range(1, nb_digits + 1):
        for password in create_passwords_fixed_size_abc(i):
            yield password


def create_passwords_fixed_size_abc(nb_digits):
    for i in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321':
        if nb_digits > 1:
            for password in create_passwords_fixed_size_abc(nb_digits - 1):
                yield password + i
        else:
            yield i


def get_passwords(filename):
    """get_passwords
    Get the passwords from a file
    :param filename: The name of the file which stores the passwords
    :return: The set of passwords
    """
    passwords = set()
    with open(filename, "r") as f:
        for line in f:
            passwords.add(line.strip())
    return passwords


replace_dict = {'a': '@', 'b': '8', 'e': '3', 'g': '6', 'i': '1', 'l': '1',
                'o': '0', 's': '$', 't': '7'}


def get_leet_words(word):
    current_leet_chars = get_leets_char(word[0])
    if len(word) == 1:
        for char in current_leet_chars:
            yield char
    else:
        for char in current_leet_chars:
            for end_word in get_leet_words(word[1:]):
                yield char + end_word


def get_leets_char(char):
    chars = [char]
    if char in replace_dict.keys():
        chars += replace_dict[char]
    return chars


if __name__ == "__main__":
    # First your password file, then your name
    crack = Crack(argv[1], argv[2])
    crack.crack(argv[3])
