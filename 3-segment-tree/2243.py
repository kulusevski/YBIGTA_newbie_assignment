from lib import SegmentTree
import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


def main() -> None:
    input = sys.stdin.readline
    N = int(input())
    M = 1000000
    
    arr = [0]*(M+1)
    seg = SegmentTree(
        arr = arr,
        func = lambda x, y: x+y,
        convert = lambda x: x,
        default_value = 0)
    
    def find_idx(idx: int, node = 1, start = 0, end = M) -> int:
        if start == end:
            return start
        mid = (start + end) // 2
        left_sum = seg.tree[node*2]
        if idx  <= left_sum:
            return find_idx(idx, node*2, start, mid)
        else:
            return find_idx(idx - left_sum, node*2 +1, mid+1, end)
        
    for _ in range(N):
        q = list(map(int, input().split()))
        
        if q[0] == 1:
            idx = q[1]
            if idx > seg.tree[1]:
                continue
            taste = find_idx(idx)
            seg.update(1, 0, M, taste, arr[taste] - 1)
            arr[taste] -= 1
            print(taste)
            
        else:
            B, C = q[1], q[2]
            if 1 <= B <= M:
                seg.update(1, 0, M, B, arr[B] + C)
                arr[B] += C            
    


if __name__ == "__main__":
    main()