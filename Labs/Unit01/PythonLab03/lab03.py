def to_celsius(temps):
    return [(i-32)*5/9 for i in temps]

def remove_email_domains(emails):
    return [e.split('@')[0] for e in emails]
            
def get_students(schools, students):
    return [i for i in students if i['school'] in schools]

def average_math_scores(students):
    math_students = list(filter(lambda x : 'math' in x, students))
    return sum(i['math'] for i in math_students)/len(math_students)

if __name__=='__main__':
    temps = [32, 68, 95, 104]
    print(to_celsius(temps))

    emails = ["user1@example.com", "user2@example.com",
    "user3@gmail.com", "user4@example.com"]
    result = remove_email_domains(emails)
    print(result)

    schools = ['Menlo', 'Sacred Heart']
    students = [{'name': 'Alice', 'grade': 9, 'school': 'Menlo'},
    {'name': 'Bob', 'grade': 10, 'school': 'Sacred Heart'},
    {'name': 'Charlie', 'grade': 9, 'school': 'Menlo'},
    {'name': 'Delta', 'grade': 9, 'school': 'Sacred Heart'},
    {'name': 'Epsilon', 'grade': 9, 'school': 'Nueva'}]
    print(get_students(schools, students))

    students = [{'name': 'Alice', 'math': 85, 'science': 92},
    {'name': 'Bob', 'science': 88},
    {'name': 'Charlie', 'math': 90, 'science': 78},
    {'name': 'Delta', 'math': 94, 'science': 78}]
    print(average_math_scores(students))