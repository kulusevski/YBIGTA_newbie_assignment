from lib import SegmentTree
import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


def main() -> None:
    '''
    입력을 처리하고 세그먼트 트리를 이용한 연산 수행함

    세그먼트 트리를 사용하여 크게 두 가지 유형의 연산을 처리:
    1. 특정 idx에 해당하는 사탕을 제거 (쿼리 유형 1, if문)
    2. 특정 종류의 사탕 개수를 추가하거나 갱신 (쿼리 유형 2, else문)
    
    입력:
    첫째 줄에 수정이가 사탕상자에 손을 댄 횟수(쿼리의 수) n(1 ≤ n ≤ 100,000)이 주어진다. 
    다음 n개의 줄에는 두 정수 A, B, 혹은 세 정수 A, B, C가 주어진다. 
    - A가 1인 경우는 사탕상자에서 사탕을 꺼내는 경우이다. B는 꺼낼 사탕의 순위를 의미한다. 사탕상자에서 한 개의 사탕이 꺼내지게 된다. 
    - A가 2인 경우는 사탕을 넣는 경우이다. 이때에는 두 정수가 주어지는데, B는 넣을 사탕의 맛을 나타내는 정수이고 C는 그러한 사탕의 개수이다. 
        - C가 양수일 경우에는 사탕을 넣는 경우이고, 음수일 경우에는 빼는 경우이다. 

    출력:
    A가 1인 모든 입력에 대해서, 꺼낼 사탕의 맛의 번호를 출력

    예제:
    입력:
        6
        2 1 2
        2 3 3
        1 2
        1 2
        2 1 -1
        1 2
        
    출력:
        1
        3
        3
    '''
    
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
        '''
        주어진 idx에 해당하는 사탕의 종류(맛 번호)를 recursive하게 찾는 함수.

        Args:
            idx: 찾고자 하는 사탕의 순위
            node: 세그먼트 트리의 현재 노드 인덱스 (default: 1)
            start: 현재 세그먼트의 시작 인덱스 (default: 0)
            end: 현재 세그먼트의 끝 인덱스 (default: M)

        Returns:
            int: 주어진 순위에 해당하는 사탕의 종류(맛 번호)
        '''
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