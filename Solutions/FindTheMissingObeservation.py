from typing import List


class Solution:
    def missingRolls(self, rolls: List[int], mean: int, n: int) -> List[int]:
        m = len(rolls)
        sumlambda = mean*(n+m) - sum(rolls)
        x = sumlambda//n
        if x > 6 or x < 1:
            return []
        if x == 6 and sumlambda%6:
            return []
        rem = sumlambda - x*n
        delta = 6-x
        otherDigits = {}
        while delta > 0 and rem > delta:
            counttemp = rem//delta
            temp = x + delta
            otherDigits[temp] = counttemp
            delta -= 1
            rem  = rem - counttemp*temp
            if rem%delta == 0:
                break

        countx = n - sum(otherDigits.values())
        answer = []
        answer.extend([x]*countx)
        for key , value in otherDigits.items():
            answer.extend([key]*value)
        if rem:
            for i in range(rem):
                answer[i] = answer[i]+1
        return answer


if __name__ == "__main__":
    rolls = [1,5,6]
    mean = 3
    n = 4
    s = Solution()
    print(s.missingRolls(rolls, mean, n))