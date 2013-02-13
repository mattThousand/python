import sys
 
def solve(used, edges, k):
    used[k]=True
    count=0
    nodes=1
    for e in edges[k]:
        if not used[e]:
            (p,q)=solve(used,edges,e)
            count=count+p
            if q:
                count=count+1
            else:
                nodes=nodes+1
    if nodes%2==0:
        return (count, True)
    else:
        return (count, False)
 
 
def main():
    line = sys.stdin.readline().strip()
    [n, m] = [int(i) for i in line.split()]
    edges = [[] for i in xrange(0, n + 1)]
    while m > 0:
        m = m - 1
        line = sys.stdin.readline().strip()
        [p, q] = [int(i) for i in line.split()]
        edges[p].append(q)
        edges[q].append(p)
    used = [False] * (n + 1)
    print edges
    print solve(used, edges, 1)[0]
 
if __name__ == '__main__':
    main()