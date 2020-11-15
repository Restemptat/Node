1. Итератор

class reverse_iter:
 
    def __init__(self, arr):
        self.count = 0
        self.arr = arr
        pass
    def __iter__(self):
        return self
    def __next__(self):
        if self.count < len(self.arr):
            next_value = self.arr[len(self.arr) - 1 - self.count]
            self.count += 1
            return next_value
        else:
            raise StopIteration
 
    def __str__(self):
        return str(self.arr)
    pass


2. Генератор

def integers():
    i = 0
    while True:
        i += 1
        yield i

def squares():
    for i in integers():
        yield i * i

def take(n, generator):
    my_list = []
    i = 0
    while i < n:
        my_list.append(next(generator))
        i += 1
    return my_list


3. Наследование

class Planet:
    Population = []
    def add_animal(self, object):
        self.Population.append(object)
    def count_animals(self):
        return len(self.Population)
    def __str__(self):
        arr = [0, 0, 0]
        for anim in self.Population:
            if type(anim) == Dog:
                arr[0] += 1
            elif type(anim) == Cat:
                arr[1] += 1
            elif type(anim) == Snake:
                arr[2] += 1
        return f"dogs: {arr[0]}, cats: {arr[1]}, snakes: {arr[2]}"

class Animal:
    def __init__(self, age, weight):
        self.age = age
        self.weight = weight
    weight = None
    age = None

class Cat(Animal):
    def __init__(self, age, weight):
        super().__init__(age, weight)
    pass

class Dog(Animal):
 
    def __init__(self, age, weight):
        super().__init__(age, weight)
    pass

class Snake(Animal):
    def __init__(self, age, weight):
        super().__init__(age, weight)
    pass