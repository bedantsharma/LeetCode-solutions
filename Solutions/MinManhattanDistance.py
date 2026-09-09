import sys
from typing import List

class Solution:

    def minExceptI(self, tt: str, i: int) -> int:
        if tt == "u":
            return self.SecondMinU if i == self.minUIndex else self.minU
        else:
            return self.SecondMinV if i == self.minVIndex else self.minV

    def maxExceptI(self, tt: str, i: int) -> int:
        if tt == "u":
            return self.SecondMaxU if i == self.maxUIndex else self.maxU
        else:
            return self.SecondMaxV if i == self.maxVIndex else self.maxV

    def minimumDistance(self, points: List[List[int]]) -> int:
        def getMH(i: int) -> int:
            umin, umax = self.minExceptI("u", i), self.maxExceptI("u", i)
            vmin, vmax = self.minExceptI("v", i), self.maxExceptI("v", i)
            return max(umax - umin, vmax - vmin)

        transformation = [(x - y, x + y) for x, y in points]
        us = [t[0] for t in transformation]
        vs = [t[1] for t in transformation]

        self.minU, self.maxU = min(us), max(us)
        self.minV, self.maxV = min(vs), max(vs)

        self.minUIndex, self.maxUIndex = us.index(self.minU), us.index(self.maxU)
        self.minVIndex, self.maxVIndex = vs.index(self.minV), vs.index(self.maxV)

        # second min/max = extreme value with that ONE specific index removed
        self.SecondMinU = min(u for idx, u in enumerate(us) if idx != self.minUIndex)
        self.SecondMaxU = max(u for idx, u in enumerate(us) if idx != self.maxUIndex)
        self.SecondMinV = min(v for idx, v in enumerate(vs) if idx != self.minVIndex)
        self.SecondMaxV = max(v for idx, v in enumerate(vs) if idx != self.maxVIndex)

        return min(getMH(i) for i in range(len(transformation)))