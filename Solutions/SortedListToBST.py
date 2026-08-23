# Definition for singly-linked list.
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
from typing import Optional, List


class Solution:
    def listToBst(self,list: Optional[List[int]]) -> Optional[TreeNode]:
        if not list or len(list) == 0:
            return None
        n = len(list)
        if n == 1:
            return TreeNode(list[0])
        if n == 2:
            t1 = TreeNode(list[0])
            t2 = TreeNode(list[1])
            t2.left = t1
            return t2
        m = TreeNode(list[n//2])
        m.left = self.listToBst(list[:n//2])
        m.right = self.listToBst(list[n//2:])
        return m

    def sortedListToBST(self, head: Optional[ListNode]) -> Optional[TreeNode]:
        arr = []
        while head :
            arr.append(head.val)
            head = head.next
        return self.listToBst(arr)
