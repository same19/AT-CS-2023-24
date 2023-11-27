def alpha_slices():
    first_ten = "abcdefghij"
    print(first_ten[:3])
    print(first_ten[::4])
    print(first_ten[4:])

def this_to_that(str):
    return str.replace('this', 'that')

def clean_string(str):
    return str.split().join(" ")

def count_email_domains(emails):
    domains = {}
    for e in emails:
        domain = e.split("@")[1]
        if domain in domains:
            domains[domain] += 1
        else:
            domains[domain] = 1
    return domains

def pet_names():
    pets = {}
    pets["Ziggie"] = "canary"
    pets["Stripey"] = "cat"
    pets["Auggie"] = "dog"
    for key, value in pets.items():
        print(key, " is a ", value)

def are_anagrams(a, b):
    a_copy = list(a)
    b_copy = list(b)
    for letter in a_copy:
        if letter in b_copy:
            a_copy = a_copy[1:]
            b_copy.remove(letter)
        else:
            return False
    if len(b_copy)==0:
        return True
    return False

def are_anagrams_with_dictionaries(a,b):
    letters = {}
    for letter in a:
        if letter in letters:
            letters[a] += 1
        else:
            letters[a] = 1
    for letter in b:
        if letter in letters:
            letters[b] -= 1
        else:
            letters[b] = -1
    for value in letters.values():
        if value != 0:
            return False
    return True