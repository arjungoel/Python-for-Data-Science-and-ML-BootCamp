# Abstract class and Abtsract method in Python...

from abc import ABC, abstractmethod

#Enforcing Abstraction...
class Animal(ABC):
    @abstractmethod     #using abstractmethod as a decorator...
    def move(self):
        pass


class Human(Animal):
    def move(self):
        print("The human can run and speak")


class Snake(Animal):
    def move(self):
        print("The Snake can bite and crawl")



def main():

# if we create object for animal also and still want to achieve abtsraction...
    #animal = Animal()
    #animal.move()
    human = Human()
    human.move()
    snake = Snake()
    snake.move()


if __name__ == "__main__":
    main()


    
