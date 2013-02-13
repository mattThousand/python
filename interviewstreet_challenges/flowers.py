import sys

lines=sys.stdin.readlines()
n,k=map(int, lines[0].strip().split())
prices=sorted(map(int, lines[1].strip().split()))

def get_cost(n, k, prices):
    bought=0
    spent=0
    if n<=k:
        return sum(prices[0:n])
    else:
        coef=1
        for p in prices:
            if bought==k:
                spent+=coef*p
                bought+=1
                coef+=1
                bought=0
            else:
                spent+=coef*p
                bought+=1
        return spent
    
if __name__ == '__main__':
    print get_cost(n,k,prices)
    
