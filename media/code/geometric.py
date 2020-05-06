import math
n=int(input("enter the term"))
if(n%2==0):
    number=int(n/2)
    x=number-1
    k=3
    output=x
    print(output)
else:
    number=int((n+1)/2)
    x=number-1
    k=2
    output=2*x
    print(output)
    
