# functional programming in python using map(),reduce() and filter()....


seq = [1,2,3,4,5]

#apply map() function
result= list(map(lambda num:num*3,seq))

#apply filter() function
result1 = list(filter(lambda num: num%2==0,seq))

print(result)
print(result1)

# map() and filter() are useful when we use to work with 'Pandas'.
# seq is an iterable object.
