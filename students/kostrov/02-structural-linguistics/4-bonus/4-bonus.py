VOWELS = {'a', 'e', 'i', 'o', 'u'}

def get_first_vowel_index(string):
    for i, char in enumerate(string):
        if char in VOWELS: return i
    return -1

def shmify(string):
    words = string.split(' ')
    is_capitalized = words[-1][0].isupper()
    last_word = words[-1].lower()
    
    if last_word[:2] == 'sh': return string

    shm_token = 'sm' if 'sh' in last_word else 'shm'    
    shmified = shm_token + last_word[get_first_vowel_index(last_word):]

    output = words[:-1] + ([shmified.capitalize()] if is_capitalized else [shmified])
    return ' '.join(output)


print(shmify('table'))
print(shmify('apple'))
print(shmify('shmaltz'))
print(shmify('Ashmont'))
print(shmify('Johnny Allen Hendrix'))