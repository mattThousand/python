import sys

def main():
    
    lines=sys.stdin.readlines()
    
    n,k=map(int, lines[0].strip().split())
    substrings=[[] for i in xrange(n)]
    index=0
    for line in lines[1:n+1]:
        line=line.strip()
        for letter in xrange(1,len(line)+1):
            substrings[index].append(line[:letter])
        for letter in xrange(len(line)):
            if line[letter:] not in substrings[index]:
                substrings[index].append(line[letter:])
        index+=1
    substrings.sort(key=lambda x:len(x))
    pals=[]    
    for idx in reversed(xrange(len(substrings))):
        for s in substrings[idx]:
            for group in substrings:
                if group!=substrings[idx]:
                    for p in group:
                        if list(s+p)==list(reversed(list(s+p))):
                            pals.append(len(s+p))
                            break
                        else:
                            continue
    return max(pals)


if __name__ == '__main__':
    main()