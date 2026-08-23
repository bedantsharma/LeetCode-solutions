from collections import deque
class Solution:

    def getSmallestString(self, n: int, k: int) -> str:
        answer = [1]*n
        k -= n
        for i in range(n-1,-1,-1):
            if k > 0:
                value = min(25,k)
                answer[i] = answer[i] + value
                k -= value
        return ''.join(chr(96 + i) for i in answer)

if __name__ == "__main__":
    s = Solution()
    sol=s.getSmallestString(3,27)
    print(sol)
