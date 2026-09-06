from typing import List


class Solution:
    def largestPerimeter(self, nums: List[int]) -> int:
        nums.sort(reverse=True)
        print(nums)
        return sum(nums)

if __name__ == "__main__":
    s = Solution()
    print(s.largestPerimeter([2,1,2]))
