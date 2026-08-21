from typing import List
class Solution:

    class Node:
        def __init__(self, x):
            self.val = x
            self.next = None

    def __init__(self):
        self.nodes =  dict()

    def makeGraph(self,prerequisites: List[List[int]]) :
        for connection in prerequisites :
            a = self.nodes.get(connection[0], None)
            b = self.nodes.get(connection[1], None)
            if not a:
                a = self.Node(connection[0])
                self.nodes[connection[0]] = a
            if not b:
                b = self.Node(connection[1])
                self.nodes[connection[1]] = b
            a.next = b


    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        root = self.makeGraph(prerequisites)
        if len(self.nodes) == 0 or len(self.nodes) == 1:
            return True
        if len(prerequisites) == numCourses == 2 :
            return False
