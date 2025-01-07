def count_characters(word):
    char_count = {}
    for char in word:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    return char_count

def anagramsearch2(wordfile, dictionary,output_file):
    
    with open(wordfile, 'r') as f:
        worddict=[]
        for word in f:
            word = word.strip() 
            sorted_key = ''.join(sorted(word.lower()))
            sortedwordcnt = count_characters(sorted_key)
            worddict.append(sortedwordcnt)

    new_dictionary = []
    with open(dictionary, 'r') as d:
        for word in d:
            word = word.strip()  
            sorted_key = ''.join(sorted(word.lower()))
            sortedwordcnt = count_characters(sorted_key)
            new_dictionary.append([sortedwordcnt,word])
            
    points_dict = {
    'a': 1, 'e': 1, 'h': 1, 'i': 1, 'n': 1, 'o': 1, 'r': 1, 's': 1, 't': 1,
    'c': 2, 'd': 2, 'l': 2, 'm': 2, 'u': 2,
    'b': 3, 'f': 3, 'g': 3, 'p': 3, 'v': 3, 'w': 3, 'y': 3,
    'j': 4, 'k': 4, 'q': 4, 'x': 4, 'z': 4
    }

    ans=[]
    for sortedwordcnt in worddict:
        max_word = ''
        max_score = 0

        for dict in new_dictionary:
            is_anagram=True
            for char,count in dict[0].items():
                if char not in sortedwordcnt.keys() or count>sortedwordcnt[char]:
                    is_anagram=False
                    break
            if is_anagram:
                point=0
                for char in dict[0].keys():
                    point+=points_dict[char]*dict[0][char]
                
                if max_score<point:
                    max_score=point
                    max_word=dict[1]
        ans.append(max_word)
    with open(output_file, 'w') as out:
        for word in ans:
            out.write(word + '\n')


wordfile = input("Word file: ")
dictionary = input("Dictionary file: ")
output_file = input("Output file: ")

anagramsearch2(wordfile, dictionary, output_file)
