from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Callable


"""
TODO:
- SegmentTree 구현하기
"""


T = TypeVar("T")
U = TypeVar("U")


class SegmentTree(Generic[T, U]):
    def __init__(self,
                 arr: list[T],
                 func: Callable[[U,U], U],
                 convert: Callable[[T],U],
                 default_value: U
                 ):
        '''
        arr: 입력될 리스트, 입력값은 T 타입
        func: 사용될 함수
        convert: 입력 리스트(T타입)을 U 타입으로 변환하는 함수
        default_value: 쿼리 범위 밖의 값일 때 return할 기본값
        
        tree의 크기는 통상적으로 사용되는 4n으로 둠  
        '''
        
        self.arr = arr
        self.n = len(arr)
        self.func = func
        self.convert = convert
        self.default_value = default_value
        self.tree = [default_value] * (4 * self.n)
        self.build(node = 1, start = 0, end = self.n - 1)
        
    
    def build(self,
              node: int, 
              start: int, 
              end: int):
        """
        트리를 초기화하고 노드를 처음부터 build하기
        
        leaf node에 도달하면 arr의 시작값 저장
        구간을 왼쪽/오른쪽 자식으로 분할해 recursive하게 내려감
        parents 노드는 child 노드값을 func통해서 저장
        
        node: 현재의 index
        """
        
        if start == end:
            self.tree[node] = self.convert(self.arr[start])
            
        else:
            mid = (start + end) //2
            self.build(node*2, start, mid)
            self.build(node*2+1, mid +1, end)
            self.tree[node] = self.func(self.tree[node*2], self.tree[node*2 + 1])
     
    def update(self,
               node:int,
               start: int,
               end: int,
               idx: int,
               value: T):
        '''
        특정 index(idx) 위치의 값을 value로 변경
        
        leaf node에 도달하면 value 갱신
        현재 구간을 더 작은 구간으로 나눌 수 있으면, 왼쪽/오른쪽 child로 내려가 recursion
        parents node로 올라오면서 func함수를 사용해 병합하면서 node값 갱신
        '''
        
        if start == end:
            self.tree[node] = self.convert(value)
        
        else:
            mid = (start+end) // 2
            if start <= idx and idx <= mid:
                self.update(node*2, start, mid, idx, value)
        
            else:
                self.update(node*2 +1, mid +1, end, idx, value)
        
            self.tree[node] = self.func(self.tree[node*2], self.tree[node*2 +1])
        
    
    def query(self,
              node: int,
              start: int,
              end: int,
              l: int,
              r: int) -> U:
        '''
        현재 구간이 query 구간을 벗어나면 return default_value 
        현재 구간이 query 구간 내 존재하면 해당 node값 반환
        현재 구간이 query 구간에 걸쳐있으면 왼/오른쪽 child로 내려가 recursion
        
        returns:
            [l, r] 구간에 해당하는 병합 결과
        '''
        
        if r < start or end < l:
            return self.default_value
        
        if l <= start and end <= r:
            return self.tree[node]
        
        mid = (start + end)//2
        left_value = self.query(node*2, start, mid, l, r)
        right_value = self.query(node*2 + 1, mid + 1, end, l, r)
        return self.func(left_value, right_value)


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
