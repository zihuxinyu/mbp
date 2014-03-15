__author__ = 'weibaohui'
# coding: utf-8
import random
import string
#python3中为string.ascii_letters,而python2下则可以使用string.letters和string.ascii_letters
def GenPassword(length):
    chars = string.ascii_letters + string.digits
    #return ''.join([random.choice(chars) for i in range(length)])  #得出的结果中字符会有重复的
    return ''.join(random.sample(chars, 15))#得出的结果中字符不会有重复的