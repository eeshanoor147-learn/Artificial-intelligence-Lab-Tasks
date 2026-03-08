# FizzBuzz game adding old+curren 
old=0
for i in range(1,101):
    total=old+i
    if (total%3==0) and (total %5==0):
        print("FizzBuzz")
    elif total%3==0:
        print("fizz")    
    elif total%5==0:
        print("buzz")  
    else:
        print(total)   
    old=i
    
# fizzbuzz simple without add old and new value  for my own ease
for i in range(1,101):
    if (i%3==0) and (i %5==0):
        print("FizzBuzz")
    elif i%3==0:
        print("fizz")    
    elif i%5==0:
        print("buzz")  
    else:
        print(i)   
    