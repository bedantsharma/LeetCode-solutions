from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        # number of rows is m and number of columns is n
        m,n = len(matrix),len(matrix[0])

        def binarySearch(l:List[int],targe:int)->bool:
            pass

        if m <= 1:
            return binarySearch(matrix[0],target)

        # first find the col that the answer might be in.
        first = 0
        last = m

        while True:
            mid = (first + last)//2
            if mid == last - 1:
                break
            ele1 = matrix[mid][0]
            ele2 = matrix[mid+1][0]
            if ele1 <= target and target <= ele2:
                break
            elif target < ele1:
                last = mid
            elif target > ele1:
                first = mid
