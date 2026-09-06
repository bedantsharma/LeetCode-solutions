from typing import List
from collections import Counter


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        map_p = Counter(p)
        map_s = Counter(s[:len(p)])
        answer = []
        difference_map = {}
        def zero(df:dict):
            # O(26) time complexity
            for i in df.values():
                if i != 0:
                    return False
            return True
        def update(df:dict, ch1:str, ch2:str):
            df[ch1] = df[ch1] - 1
            df[ch2] = df[ch2] + 1
            return df
        for i in range(ord('a'), ord('z')+1):
            ch = chr(i)
            difference_map[ch] = map_s[ch] - map_p[ch]
        if zero(difference_map):
            answer.append(0)
        for i in range(len(s)-len(p)):
            ch1 = s[i]
            ch2 = s[i+len(p)]
            difference_map = update(difference_map,ch1,ch2)
            if zero(difference_map):
                answer.append(i+1)
        return answer

if __name__ == '__main__':
    s = Solution()
    print(s.findAnagrams("baa", "aa"))


