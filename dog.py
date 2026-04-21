# Create a dog class with a dog's name and age and then include functions to make the dog sit, roll_over and update medications
class Dog():
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.meds = 0

    def sit(self):
        print(self.name.title(), " is now sitting", sep='')

    def roll_over(self):
        print(self.name.title(), " rolled over!", sep='')

    def update_medications(self, medications):
        self.meds = medications
        print(self.name.title(), ' is currently on ', self.meds, ' medications', sep='')

# Create a child class called Labrador using the parent class Dog
class Labrador(Dog):
    def __init__(self, name, age):
        super().__init__(name, age)


my_dog = Labrador('Mikasa', 5)
print('Name: ', my_dog.name.title(), '\n', 'Age: ', my_dog.age, sep='')
my_dog.sit()
my_dog.roll_over()
my_dog.update_medications(2)