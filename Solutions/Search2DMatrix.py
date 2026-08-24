import doctest
from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        # number of rows is m and number of columns is n
        m,n = len(matrix),len(matrix[0])

        def binarySearch(l:List[int],targe:int)->bool:
            low = 0
            high = len(l)-1
            while low <= high:
                mid = (low + high)//2
                if target == l[mid]:
                    return True
                elif target < l[mid]:
                    high = mid - 1
                else:
                    low = mid + 1
            return False

        if m <= 2:
            return binarySearch(matrix[0],target) or binarySearch(matrix[-1],target)
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

        flag = False
        if mid+1 < last and matrix[mid+1][0] == target:
            flag = True

        return binarySearch(matrix[mid],target) or flag

if __name__ == "__main__":
    matrix = [[1],[3],[5]]
    s = Solution()
    print(s.searchMatrix(matrix,5))
