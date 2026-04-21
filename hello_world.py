# Functions
def get_age():
    age = int(input('How old are you? '))
    return age

# Using line change & Methods to alter the name
message, name, age = 'Hello, World! ', 'Sash', 27
print(message.strip(), '\n', name.title(), '\n', name.upper(), '\n', name.lower(), '\n' + str(age) + ' years old', sep='')

# Lists
fruits = ['apple', 'banana', 'cherry']  # If you want an immutable sequence, use a tuple: fruits = ('apple', 'banana', 'cherry')
fruits.append('orange') # Adding to the end of the list
fruits[1] = 'guava'
fruits.insert(1, 'pear')
fruits.remove('cherry') # We can use del fruits[3] if we know the position but are not aware of the value
print(fruits, '\n', sorted(fruits, reverse=True), '\n', fruits[0], '\n', fruits[2:3], '\n', fruits[-1].title(), sep='')

fruits.sort(reverse=True) # Cannot print directly since sort() returns None and changes the list permanently unlike sorted() which is temp
print(fruits.pop(1), '\n', fruits, sep='')

fruits.reverse() # Same idea as sort() since reverse() also changes the list permanently
print(fruits, '\n', len(fruits), sep='')

# Looping
for fruit in fruits:
    print(fruit.title())

for value in range(1,6): # We can also do list(range(2,11,2)) to create lists with even numbers
    print(value)

squares = [] # We can directly do squares = [pow(value,2) for value in range (1,11)]
for value in range(1,11):
    square = pow(value,2)
    squares.append(square)
print(squares, '\n', sum(squares), sep='') # We can use min and max as well

# Ifs
for square in squares:
    if 26 in squares:
        print(square)
    elif 25 not in squares:
        print(square)

# Dictionaries
car = {
    'make': 'Toyota',
    'model': 'Corolla',
    'year': 2022,
    'color': ['blue', 'red', 'yellow'], # List in a dictionary
    'mileage': 15000,
    'electric': False
}
del car['mileage']
print(sorted(car))

for key, value in car.items(): # If we just use the keys then just say "for key in car.keys():" and for values just say "for value in car.values()"
    if car[key] == 2022:
        print(car['make'])

# User input and while
age = get_age()
print('You have, therefore, been on this planet for ', int(age/10), ' decades', sep='')

while age >= 25: # Break, continue and flag (can be set up so that certain events occuring change its value to False which stops the entire program)
    print(age)
    age = age - 1