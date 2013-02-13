import sys


def main():
    return sum(i-k in numbers for i in numbers)

if __name__ == '__main__':
    lines=sys.stdin.readlines()
    n,k=map(int, lines[0].strip().split())
    numbers=map(int, lines[1].strip().split())
    print main()