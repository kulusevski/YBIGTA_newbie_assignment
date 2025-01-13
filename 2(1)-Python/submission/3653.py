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
    # 구현하세요!
    pass


if __name__ == "__main__":
    main()