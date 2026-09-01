def print_graph(node):
    if node is None:
        print([])
        return

    seen = set()
    result = {}
    queue = [node]

    while queue:
        current = queue.pop(0)

        if current is None:
            continue

        if current.val in seen:
            continue

        seen.add(current.val)

        result[current.val] = [
            neighbor.val
            for neighbor in current.neighbors
            if neighbor is not None
        ]

        queue.extend(
            neighbor
            for neighbor in current.neighbors
            if neighbor is not None
        )

    print([result[i] for i in sorted(result)])

class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

from typing import Optional


class Solution:
    def __init__(self):
        self.seen = []
        self.clones = dict()

    def cloneNodes(self,root):
        if not root:
            return
        if root in self.seen:
            return
        self.seen.append(root)
        self.clones[root] = Node(root.val)
        [self.cloneNodes(n) for n in root.neighbors]

    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        self.cloneNodes(node)
        for real, clone in self.clones.items():
            clone.neighbors = [self.clones.get(n) for n in real.neighbors]
        return self.clones[node]



if __name__ == '__main__':
    # Create nodes
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)

    # Create graph:
    #
    #       1
    #      / \
    #     2   4
    #      \ /
    #       3

    node1.neighbors = [node2, node4]
    node2.neighbors = [node1, node3]
    node3.neighbors = [node2, node4]
    node4.neighbors = [node1, node3]

    solution = Solution()

    cloned = solution.cloneGraph(node1)

    print_graph(cloned)
