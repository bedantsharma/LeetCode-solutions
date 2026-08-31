import math
from typing import List


class Solution:
    def missingRolls(self, rolls: List[int], mean: int, n: int) -> List[int]:
        m = len(rolls)
        sumlambda = mean*(m+n) - sum(rolls)
        x = sumlambda//n
        rem = sumlambda - x*n
        delta = 6-x
        if x > 6 or x < 1 or (x == 6 and rem):
            return []
        a1 = [x]*(n-rem)
        a2 = [x+1]*rem
        a1.extend(a2)
        return a1