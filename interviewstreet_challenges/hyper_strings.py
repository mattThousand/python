from collections import Counter
import sys

lines=sys.stdin.readlines()

a,b=map(int, lines[0].strip().split())

y=Counter(len(lines[i].strip()) for i in xrange(1,a+1))

saved={}

def f(x):
    if x in saved: return saved[x]
    if x<1: return 0
    b=y[x] if x in y else 0
    for i in y:
        b+=y[i]*f(x-i)
    saved[x]=b
    return b
x=0
for i in xrange(1,b+1):
    x+=f(i)

print (x+1) % 1000000007


