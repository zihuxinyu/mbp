from random import random
import string


def generate_code():
    '''''Function to generate a password'''
    passwd = []
    while (len(passwd) < 4):
        passwd.append(random.choice(string.digits))
    return ''.join(passwd)