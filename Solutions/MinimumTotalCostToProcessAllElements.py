class Solution:
    def minimumCost(self, nums: list[int], k: int) -> int:
        total_cost = 0
        p = 0
        running_total = k
        m = 7 + 1e9
        def update(running_total: int,p: int ,n: int) -> tuple[int,int]:
            nonlocal total_cost
            to_add = n**2 + 2*n*p + n
            to_add = to_add//2
            total_cost += to_add
            running_total += k * n
            p += n
            return running_total,p


        for num in nums:
            if running_total < num:
                if (num-running_total) % k :
                    n = 1 + (num - running_total)// k
                else:
                    n = (num - running_total)// k
                running_total, p = update(running_total, p , n)
            running_total -= num
        return int(total_cost%m)

if __name__ == "__main__":
    sol = Solution()
    nums = [100,100,100]
    k = 1
    print(sol.minimumCost(nums, k))