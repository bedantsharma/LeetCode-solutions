import sys
from typing import List

class Solution:
    def __init__(self):
        self.mat = []

    def rec(self,l1:list,l2:list,i: int,n:int,incommingMatrix:list[list[int]]) -> int:
        if self.flipAndCheck(l1,incommingMatrix):
            return len(l1)
        else:
            if i >= n:
                return sys.maxsize
            l1.append(l2[i])
            a = self.rec(l1,l2,i+1,n,incommingMatrix)
            l1.pop()
            b = self.rec(l1,l2,i+1,n,incommingMatrix)
            return min(a,b)

    def minFlips(self, mat: List[List[int]]) -> int:
        m = len(mat)
        n = len(mat[0])
        self.n = n
        self.m = m
        l2 = []
        for i in range(m):
            for j in range(n):
                l2.append((i,j))
        answer = self.rec([],l2,0,n*m,mat)
        if sys.maxsize == answer:
            return -1
        return answer

    def checkZero(self,matrix:list[list[int]])->bool:
        for row in matrix:
            for ele in row:
                if ele != 0:
                    return False
        return True

    def inBounds(self,i:int,j:int):
        return 0 <= i < self.m and 0 <= j < self.n

    def flip(self,point:tuple[int,int],matrix:list) -> list:
        m = len(matrix)
        n = len(matrix[0])
        x, y = point
        if self.inBounds(x,y):
            matrix[x][y] ^= 1
        left = (x -1,y)
        right = (x +1, y)
        top = (x,y + 1)
        bottom = (x,y - 1)
        arr = [left, right, top, bottom]
        for p in arr:
            if self.inBounds(p[0],p[1]):
                matrix[p[0]][p[1]] ^= 1
        return matrix

    def flipAndCheck(self, l1:list[tuple[int,int]],incommingMatrix)->bool:
        mat = [row.copy() for row in incommingMatrix]

        for i in l1:
            mat = self.flip(i,mat)
        return self.checkZero(mat)

if __name__ == '__main__':
    s = Solution()
    a = s.minFlips([[0,0],[0,1]])
