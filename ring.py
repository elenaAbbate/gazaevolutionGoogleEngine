"""n = 1
i = [0,1]
while n < 20:
    c = i[n-1]+i[n]
    i.append(c)
    n = n + 1
    print(i)


#e"""


# i

# 0, 1, 1, 2, 3, 5, 8, 13, 21, 34

def fib(n=50, prev1=0, prev2=1):
    if n < 3:
        return
    else
        fn = prev1 + prev2
        prev2 = prev1
        prev1 = fn
        print(fn, end=" ")
        fib(n - 1, prev1, prev2)

