# Definition for singly-linked list.
from turtle import right


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
from typing import Optional


class Solution:
    def sortedListToBST(self, head: Optional[ListNode]) -> Optional[TreeNode]:
        n = 0
        curr = head
        while curr:
            n += 1
            curr = curr.next

        def buildTree(n: int) -> Optional[TreeNode] :
            nonlocal head

            if n <= 0:
                return None

            left = buildTree(n//2) # this will consume the first n//2 elements of the linklist
            root= TreeNode(head.val)
            head = head.next
            rightSide = n - 1 - n//2
            right = buildTree(rightSide)
            root.left = left
            root.right = right
            return root
        return buildTree(n)

if __name__ == '__main__':
    arr = [1,2,3]
    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    s = Solution()
    s.sortedListToBST(head)