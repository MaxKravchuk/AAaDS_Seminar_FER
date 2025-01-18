# avl_tree.py

class AVLNode:
    """A node in the AVL tree."""
    __slots__ = ['key', 'height', 'left', 'right']

    def __init__(self, key: int):
        self.key = key
        self.height = 1  # Initial height for a new leaf node
        self.left = None
        self.right = None


class AVLTree:
    """An AVL tree implementation."""

    def __init__(self):
        self.root = None

    #####################################################
    # Utility methods
    #####################################################

    def get_height(self, node: AVLNode) -> int:
        if not node:
            return 0
        return node.height

    def get_balance(self, node: AVLNode) -> int:
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def get_min_value_node(self, node: AVLNode) -> AVLNode:
        current = node
        while current and current.left:
            current = current.left
        return current

    #####################################################
    # Rotations
    #####################################################

    def right_rotate(self, z: AVLNode) -> AVLNode:
        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def left_rotate(self, z: AVLNode) -> AVLNode:
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    #####################################################
    # Insert
    #####################################################

    def insert(self, node: AVLNode, key: int) -> AVLNode:
        """Recursively insert a new key into the subtree rooted at 'node'."""
        if not node:
            return AVLNode(key)
        elif key < node.key:
            node.left = self.insert(node.left, key)
        else:
            node.right = self.insert(node.right, key)

        # Update the height of this ancestor node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Check balance
        balance = self.get_balance(node)

        # Left Left
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)
        # Right Right
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)
        # Left Right
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        # Right Left
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def insert_key(self, key: int):
        """Public insert method that updates self.root."""
        self.root = self.insert(self.root, key)

    #####################################################
    # Delete
    #####################################################

    def delete(self, node: AVLNode, key: int) -> AVLNode:
        """Recursively delete 'key' from the subtree rooted at 'node'."""
        if not node:
            return node

        if key < node.key:
            node.left = self.delete(node.left, key)
        elif key > node.key:
            node.right = self.delete(node.right, key)
        else:
            # Node to be deleted
            if not node.left:
                temp = node.right
                node = None
                return temp
            elif not node.right:
                temp = node.left
                node = None
                return temp
            else:
                # Node with two children -> get inorder successor
                temp = self.get_min_value_node(node.right)
                node.key = temp.key
                node.right = self.delete(node.right, temp.key)

        if not node:
            return node

        # Update height
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Rebalance if needed
        balance = self.get_balance(node)

        # Left Left
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)
        # Left Right
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        # Right Right
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)
        # Right Left
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def delete_key(self, key: int):
        """Public delete method that updates self.root."""
        self.root = self.delete(self.root, key)

    #####################################################
    # Search
    #####################################################

    def search(self, node: AVLNode, key: int) -> bool:
        """Simple recursive True/False search (not used for path)."""
        if not node:
            return False
        if node.key == key:
            return True
        elif key < node.key:
            return self.search(node.left, key)
        else:
            return self.search(node.right, key)

    def search_key(self, key: int) -> bool:
        """Public search method that returns only True/False."""
        return self.search(self.root, key)

    def search_key_with_path(self, key: int):
        """
        Returns a tuple: (found_boolean, path_of_nodes),
        where path_of_nodes is the list of nodes visited 
        (in the order they were visited).
        """
        path = []
        current = self.root
        while current:
            path.append(current)
            if current.key == key:
                return True, path
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return False, path