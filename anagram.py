def anagramsearch(random_word, dictionary):
    
    sorted_word = ''.join(sorted(random_word.lower()))
    new_dictionary = {}

    with open(dictionary, 'r') as f:
        for word in f:
            word = word.strip()  
            sorted_key = ''.join(sorted(word.lower()))
            if sorted_key in new_dictionary:
                new_dictionary[sorted_key].append(word)
            else:
                new_dictionary[sorted_key] = [word]
    
    sorted_keys = sorted(new_dictionary.keys())

   
    a = 0
    b = len(sorted_keys)-1
    while a <= b:
        c = (a + b) // 2
        if sorted_keys[c] == sorted_word:
            return new_dictionary[sorted_keys[c]]
        elif sorted_keys[c] < sorted_word:
            a = c+1
        else:
            b = c-1

    return []

random_word=input("randomword: ")
dictionary=input("filename: ")
print(anagramsearch(random_word,dictionary))

    