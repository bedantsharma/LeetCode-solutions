from typing import List

class Solution:
    def peopleIndexes(self, favoriteCompanies: List[List[str]]) -> List[int]:
        sfc :List[tuple[set,int]]= [(set(x),i)for i,x in enumerate(favoriteCompanies)]
        n = len(favoriteCompanies)
        answer = []
        sfc.sort(key=lambda x: len(x[0]))
        for i in range(n):
            elei = sfc[i][0]
            flag = True
            for j in range(i+1,n):
                elej = sfc[j][0]
                if elei.issubset(elej):
                    flag = False
                    break
            if flag:
                answer.append(sfc[i][1])
        answer.sort()
        return answer


if __name__ == '__main__':
    sol = Solution()
    favoriteCompanies = [["leetcode"],["google"],["facebook"],["amazon"]]
    ans = sol.peopleIndexes(favoriteCompanies)
    print(ans)