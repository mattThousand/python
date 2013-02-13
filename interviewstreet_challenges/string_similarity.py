import sys

n=int(sys.stdin.readline().strip())

for i in xrange(n):
    string=sys.stdin.readline().strip()
    suffixes=[]
    score=1
    for l in xrange(0,len(string)):
        suffixes.append(string[l:])
    for i in suffixes:
        for j in xrange(0,len(i)):
            if j==0:
                if i[0]==string[0]:
                    score+=1
                else:
                    continue
            elif j>1:
                if i[:j]==string[:j]:
                    score+=1
                else:
                    continue
            else:
                continue
    print score