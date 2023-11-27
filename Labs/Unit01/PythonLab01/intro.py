import math

def count_duplicate(arr):
    count = 0
    temp = []
    counted = []
    for i in arr:
        if i in temp and i not in counted:
            count += 1
            counted.append(i)
        elif i in counted:
            continue
        else:
            temp.append(i)
    return count

def famous_people():
    famous_list = []
    for i in range(4):
        famous_list.append(input("Name a famous person: "))
    print(famous_list)
    famous_list.pop()
    print(famous_list)
    famous_list.pop(0)
    print(famous_list)
    name_to_remove = famous_list[0]
    famous_list.remove(name_to_remove)
    print(famous_list)
    famous_list.pop()
    print(famous_list)

def working_list():
    careers = ['Electrician', 'Scientist', 'Historian', 'Musician']
    print(careers.index('Scientist'))
    print('Scientist' in careers)
    careers.append('Truck Driver')
    careers.insert(0, 'Politician')
    for i in careers:
        print(i)

def alpha_slices():
    first_ten = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    print(first_ten[:3])
    print(first_ten[::4])
    print(first_ten[4:])

def get_prime():
    i = int(input("Enter a positive whole number: "))
    while True:
        prime = True
        for check in range(2,i):
            if i % check == 0:
                prime = False
                break
        if prime:
            return i
        i += 1

def running_sum(arr):
    return [sum(arr[:i]) for i in range(1,len(arr)+1)]

def add_digits(num):
    return int(sum((num // math.pow(10, i)) % 10 for i in range(int(math.log10(num))+2)))

if __name__ == '__main__':
    arr = [1, 1, 2, 1, 3, 2, 4, 1]
    print(count_duplicate(arr))
    famous_people()
    working_list()
    alpha_slices()
    print(get_prime())
    print(running_sum([1, 2, 3, 5]))
    print(add_digits(107190080))
