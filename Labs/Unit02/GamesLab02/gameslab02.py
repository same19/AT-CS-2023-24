def is_palindrome(word):
    if len(word) < 2:
        return True
    if word[0] == word[-1]:
        return is_palindrome(word[1:-1])
    else:
        return False
    
def permutations(string, do_print = True):
    l = []
    for i in range(len(string)):
        letter = string[i]
        new_str = string[:i] + string[i+1:]
        if len(new_str) == 0:
            if do_print:
                print(letter)
            return [letter]
        p = permutations(new_str, False)
        for w in p:
            l.append(letter + w)
            if do_print:
                print(letter + w)
    return l

def gcd(a,b):
    if a == 0:
        return b
    elif b == 0:
        return a
    elif a == 1 or b == 1:
        return 1
    
    if a > b:
        return gcd(a-b, b)
    else:
        return gcd(a, b-a)
def find_paths(maze):
    l = []
    if len(maze) == 1 and len(maze[0]) == 1:
        return maze
    #down
    if len(maze) > 1:
        l += [[maze[0][0]] + i for i in find_paths(maze[1:])]
    #right
    if len(maze[0])>1:
        temp = [maze[index][1:] for index in range(len(maze))]
        l += [[maze[0][0]] + i for i in find_paths(temp)]
    return l

def binary_strings(k, allowed_start_one = True):
    if k == 1:
        if allowed_start_one:
            return ['0', '1']
        else:
            return ['0']
    if allowed_start_one:
        return ['0' + i for i in binary_strings(k-1, True)]+['1' + i for i in binary_strings(k-1, False)]
    else:
        return ['0' + i for i in binary_strings(k-1, True)]


permutations("abcd")
print(is_palindrome("raecar"))
print(is_palindrome("racecar"))
print(is_palindrome("raceecar"))
print(gcd(12,12))
print(binary_strings(4))
arr = [[1,2,3],[4,5,6]]
print(arr)
print(find_paths(arr))


