import sys

def main():

    lines=sys.stdin.readlines()
    
    n=int(lines[0].strip())
    substrings=[]
    for i in xrange(1,n+1):
        string=lines[i].strip()
        for j in range(1,len(string)+1):
            if string[:j] not in substrings:
                substrings.append(string[:j])
        for j in range(0,len(string)):
            if string[j:] not in substrings:
                substrings.append(string[j:])
    
    substrings=sorted(substrings)
    
    num_queries=int(lines[n+1].strip())
    
    for q in xrange(num_queries):
        try:
            index=int(lines[n+q+2].strip())
            print substrings[index-1]
        except IndexError:
            print 'INVALID'
            continue


if __name__ == '__main__':
    main()