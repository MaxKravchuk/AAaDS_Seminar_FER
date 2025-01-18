import numpy as np

class BTreeNode:
    def __init__(self, t: int, leaf: bool = True):
        self.t = t
        self.leaf = leaf
        self.keys = np.full((2 * t - 1,), fill_value=-1, dtype=int)
        self.children = [None] * (2 * t)
        self.n = 0

    def __str__(self):
        valid_keys = [str(key) for key in self.keys[:self.n]]
        return f"BTreeNode(keys={valid_keys}, leaf={self.leaf})"


class BTree:
    def __init__(self, t: int):
        self.t = t
        self.root = BTreeNode(t, leaf=True)

    def traverse(self, node: BTreeNode):
        i = 0
        while i < node.n:
            if not node.leaf:
                self.traverse(node.children[i])
            print(node.keys[i], end=" ")
            i += 1
        if not node.leaf:
            self.traverse(node.children[i])

    def search(self, node: BTreeNode, k: int):
        i = 0
        while i < node.n and k > node.keys[i]:
            i += 1
        if i < node.n and node.keys[i] == k:
            return (node, i)
        if node.leaf:
            return None
        return self.search(node.children[i], k)

    def search_key(self, k: int):
        return self.search(self.root, k) is not None

    def search_key_with_path(self, k: int):
        path = []
        found = self._search_key_with_path(self.root, k, path)
        return found, path

    def _search_key_with_path(self, node: BTreeNode, k: int, path: list):
        path.append(node)
        i = 0
        while i < node.n and k > node.keys[i]:
            i += 1
        if i < node.n and node.keys[i] == k:
            return True
        if node.leaf:
            return False
        return self._search_key_with_path(node.children[i], k, path)

    def insert_key(self, k: int):
        root = self.root
        if root.n == 2 * self.t - 1:
            s = BTreeNode(self.t, leaf=False)
            s.children[0] = root
            self.split_child(s, 0)
            i = 0
            if s.keys[0] < k:
                i += 1
            self.insert_non_full(s.children[i], k)
            self.root = s
        else:
            self.insert_non_full(root, k)

    def insert_non_full(self, node: BTreeNode, k: int):
        i = node.n - 1
        if node.leaf:
            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
            node.n += 1
        else:
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            if node.children[i].n == 2 * self.t - 1:
                self.split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self.insert_non_full(node.children[i], k)

    def split_child(self, parent: BTreeNode, i: int):
        t = self.t
        node_to_split = parent.children[i]
        new_node = BTreeNode(t, leaf=node_to_split.leaf)
        new_node.n = t - 1

        for j in range(t - 1):
            new_node.keys[j] = node_to_split.keys[j + t]
        if not node_to_split.leaf:
            for j in range(t):
                new_node.children[j] = node_to_split.children[j + t]
        node_to_split.n = t - 1

        for j in range(parent.n, i, -1):
            parent.children[j + 1] = parent.children[j]
        parent.children[i + 1] = new_node

        for j in range(parent.n - 1, i - 1, -1):
            parent.keys[j + 1] = parent.keys[j]
        parent.keys[i] = node_to_split.keys[t - 1]

        parent.n += 1

    def delete_key(self, k: int):
        self._delete_internal(self.root, k)
        if self.root.n == 0 and not self.root.leaf:
            self.root = self.root.children[0]

    def _delete_internal(self, node: BTreeNode, k: int):
        t = self.t
        idx = 0
        while idx < node.n and node.keys[idx] < k:
            idx += 1

        if idx < node.n and node.keys[idx] == k:
            if node.leaf:
                for i in range(idx, node.n - 1):
                    node.keys[i] = node.keys[i + 1]
                node.n -= 1
            else:
                if node.children[idx].n >= t:
                    predecessor = self._get_predecessor(node.children[idx])
                    node.keys[idx] = predecessor
                    self._delete_internal(node.children[idx], predecessor)
                elif node.children[idx + 1].n >= t:
                    successor = self._get_successor(node.children[idx + 1])
                    node.keys[idx] = successor
                    self._delete_internal(node.children[idx + 1], successor)
                else:
                    self._merge(node, idx)
                    self._delete_internal(node.children[idx], k)
        else:
            if node.leaf:
                return
            if node.children[idx].n < t:
                self.fill_child(node, idx)
            self._delete_internal(node.children[idx], k)

    def _get_predecessor(self, node: BTreeNode):
        while not node.leaf:
            node = node.children[node.n]
        return node.keys[node.n - 1]

    def _get_successor(self, node: BTreeNode):
        while not node.leaf:
            node = node.children[0]
        return node.keys[0]

    def fill_child(self, node: BTreeNode, idx: int):
        t = self.t
        if idx > 0 and node.children[idx - 1].n >= t:
            self._borrow_from_prev(node, idx)
        elif idx < node.n and node.children[idx + 1].n >= t:
            self._borrow_from_next(node, idx)
        else:
            if idx < node.n:
                self._merge(node, idx)
            else:
                self._merge(node, idx - 1)

    def _borrow_from_prev(self, node: BTreeNode, idx: int):
        child = node.children[idx]
        sibling = node.children[idx - 1]

        for i in range(child.n - 1, -1, -1):
            child.keys[i + 1] = child.keys[i]
        if not child.leaf:
            for i in range(child.n, -1, -1):
                child.children[i + 1] = child.children[i]

        child.keys[0] = node.keys[idx - 1]
        if not sibling.leaf:
            child.children[0] = sibling.children[sibling.n]
        node.keys[idx - 1] = sibling.keys[sibling.n - 1]
        sibling.n -= 1
        child.n += 1

    def _borrow_from_next(self, node: BTreeNode, idx: int):
        child = node.children[idx]
        sibling = node.children[idx + 1]

        child.keys[child.n] = node.keys[idx]
        if not child.leaf:
            child.children[child.n + 1] = sibling.children[0]

        node.keys[idx] = sibling.keys[0]
        for i in range(1, sibling.n):
            sibling.keys[i - 1] = sibling.keys[i]
        if not sibling.leaf:
            for i in range(1, sibling.n + 1):
                sibling.children[i - 1] = sibling.children[i]
        sibling.n -= 1
        child.n += 1

    def _merge(self, node: BTreeNode, idx: int):
        child = node.children[idx]
        sibling = node.children[idx + 1]

        child.keys[self.t - 1] = node.keys[idx]
        for i in range(sibling.n):
            child.keys[i + self.t] = sibling.keys[i]
        if not child.leaf:
            for i in range(sibling.n + 1):
                child.children[i + self.t] = sibling.children[i]

        for i in range(idx + 1, node.n):
            node.keys[i - 1] = node.keys[i]
        for i in range(idx + 2, node.n + 1):
            node.children[i - 1] = node.children[i]

        child.n += sibling.n + 1
        node.n -= 1