# Abstract class and Abtsract method in Python...

class Animal:
    def move(self):
        pass


class Human(Animal):
    def move(self):
        print("The human can run and speak")


class Snake(Animal):
    def move(self):
        print("The Snake can bite and crawl")



def main():
    human = Human()
    human.move()
    snake = Snake()
    snake.move()


if __name__ == "__main__":
    main()


    
