# As a "for" Loop...
'''
squares = []
for x in range(10):
    squares.append(x*x)

print(squares)
'''

# use of List Comprehension....

squares = [x*x for x in range(10)]
print(squares)


# format of list comprehension...
(values) = [ (expression) for (value) in (collection)]

# Transforms into "for" loop:

(values) = []
for (value) in (collection):
    (values).append((expression))



# it works in both directions...


# Ques:- how can we extend this pattern to actually include filtering?

# Ans:- Filtering is going to make the list comprehensions that we can write a lot more powerful and a lot more flexible.



#List comprehensions: Filtering
even_squares = [x*x for x in range(10) if x%2==0]


even_squares = []
for x in range(10):
    if x%2 == 0:
        even_squares.append(x*x)



#format of list comprehension filtering...
values = [ (expression) for value in collection if condition]


# Transforms into "for" loop:

values = []
for value in collection:
    if condition:
        values.append(expression)


# One downside of list comprehensions is that they are more terse than for loops. They can feel or they can get a little bit overwhelming if someone is not familiar with them.
# The list comprehensions can also be nested so that we can list comprehensions inside list comprehensions.
