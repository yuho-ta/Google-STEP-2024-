import sys
import re

def binary_search(new_dictionary,sorted_word):
    sorted_keys = sorted(new_dictionary.keys())
   
    left = 0
    right = len(sorted_keys) - 1
    while left <= right:
        middle = (left + right) // 2
        if sorted_keys[middle] == sorted_word:
            return new_dictionary[sorted_keys[middle]]
        elif sorted_keys[middle] < sorted_word:
            left = middle + 1
        else:
            right = middle - 1
    return None


def anagram_search(random_word, dictionary):

    #特殊記号を削除、ソート
    code_regex = re.compile('[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]')
    cleaned_word=code_regex.sub('',random_word)
    sorted_word = ''.join(sorted(cleaned_word.lower()))

    #辞書ファイルの単語をanagramごとにまとめる
    new_dictionary = {}
    with open(dictionary, 'r') as f:
        for word in f:
            word = word.strip()  
            sorted_key = ''.join(sorted(word.lower()))
            if sorted_key in new_dictionary:
                new_dictionary[sorted_key].append(word)
            else:
                new_dictionary[sorted_key] = [word]
    
    return binary_search(new_dictionary,sorted_word)

if __name__=='__main__':
    random_word=sys.argv[1]
    dictionary=sys.argv[2]
    print(anagram_search(random_word,dictionary))

    