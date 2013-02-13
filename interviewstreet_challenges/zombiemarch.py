import sys
page_rank_iteration_round = 50

def main():
    # read t
    line = sys.stdin.readline()
    t = int(line)
    for _ in range(t):
        # test time
        # print "start: %d" % time.time()
        # read n, m, k
        line = sys.stdin.readline().strip()
        (n, m, k) = (int(i) for i in line.split())
        # define node degree, and edges
        degree = [0] * n
        edges = [[] for i in xrange(0, n)]
        # read edges
        for i in xrange(0, m):
            line = sys.stdin.readline()
            (p, q) = (int(x) for x in line.split())
            degree[p] += 1
            degree[q] += 1
            edges[p].append(q)
            edges[q].append(p)
        # define zombie number
        num = [[0.0] * n for i in xrange(0, 2)]
        # read initial zombie number
        for i in xrange(0, n):
            line = sys.stdin.readline()
            num[0][i] = float(line)
        # end input time
        # print "end input: %d" % time.time()
        # enumarate the process
        k = min(k, page_rank_iteration_round)
        now, next_ = 0, 1
        for _ in range(k):
            for i in xrange(0, n):
                num[next_][i] = 0
                for j in edges[i]:
                    num[next_][i] = num[next_][i] + num[now][j] / degree[j]
            now, next_ = next_, now
        # sort the result
        num[now].sort(reverse = True)
        # end compute time
        # print "end compute: %d" % time.time()
        # output the result
        for i in num[now][0:5]:
            print int(round(i)),
        print

if __name__ == '__main__':
    main()