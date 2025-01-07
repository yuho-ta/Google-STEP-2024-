import sys

def count_characters(file):
    with open(file, 'r') as f:
        word_dict=[]
        for word in f:
            word = word.strip() 
            sorted_key = ''.join(sorted(word.lower()))
            char_count = {}
            for char in sorted_key:
                if char in char_count:
                    char_count[char] += 1
                else:
                    char_count[char] = 1
            word_dict.append([char_count,word])
    return word_dict

def dict_sort_point(dictionary):
    points_dict = {
    'a': 1, 'e': 1, 'h': 1, 'i': 1, 'n': 1, 'o': 1, 'r': 1, 's': 1, 't': 1,
    'c': 2, 'd': 2, 'l': 2, 'm': 2, 'u': 2,
    'b': 3, 'f': 3, 'g': 3, 'p': 3, 'v': 3, 'w': 3, 'y': 3,
    'j': 4, 'k': 4, 'q': 4, 'x': 4, 'z': 4
    }

    points_list=[0] * 26     

    for char, points in points_dict.items():
        index = ord(char) - ord('a')
        points_list[index] = points
    
    for word_dict in dictionary:
         point = 0
         for char,count in word_dict[0].items():
              point += points_list[ord(char) - ord('a')]*count
         word_dict.append(point)
    
    dictionary = sorted(dictionary, key = lambda x: x[2],reverse=True)
    
    return dictionary


def anagram_search2(word_file, dictionary,output_file):
    
    word_dict=count_characters(word_file)

    dictionary=dict_sort_point(count_characters(dictionary))
    
    ans=[]
    for sorted_wordcnt in word_dict:
        max_word = ''
        max_score = 0
        for dict in dictionary:
            is_anagram = True
            for char,count in dict[0].items():
                if char not in sorted_wordcnt[0].keys() or count>sorted_wordcnt[0][char]:
                    is_anagram = False
                    break
            if is_anagram:
                if max_score < dict[2]:
                    max_score = dict[2]
                    max_word = dict[1]
        ans.append(max_word)
    with open(output_file, 'w') as out:
        for word in ans:
            out.write(word + '\n')

if __name__=='__main__':
    word_file=sys.argv[1]
    dictionary=sys.argv[2]
    output_file=sys.argv[3]
    print(anagram_search2(word_file,dictionary,output_file))
