import sys

def substr(string):
    j=1
    a=list()
    while True:
        for i in xrange(len(string)-j+1):
            a.append(string[i:i+j])
        if j==len(string):
            break
        j+=1
    return a
    

def main():
    lines=sys.stdin.readlines()
    t=int(lines[0].strip())
    for line in lines[1:t+1]:
        k=int(line.strip().split()[0])
        p=line.strip().split()[1]
        q=line.strip().split()[2]
        p_substrings=[i for i in substr(p)]
        q_substrings=[i for i in substr(q)]
        p_substrings.sort(key=lambda x: len(x))
        q_substrings.sort(key=lambda x: len(x))
        candidates=[]
        for p in p_substrings:
            for q in q_substrings:
                score=0
                if len(p)==len(q):
                    for i in xrange(len(p)):
                        if p[i]!=q[i]:
                            score+=1
                        else:
                            continue
                    if score==k:
                        candidates.append(len(q))
                    else:
                        continue
        print max(candidates)


if __name__ == '__main__':
    main()