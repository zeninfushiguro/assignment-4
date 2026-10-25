class DoctorNode:
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None


class DoctorTree:
    def __init__(self):
        self.root = None

    def _find(self, node, name):
        """Recursively find the node with the given name, or None."""
        if node is None:
            return None
        if node.name == name:
            return node
        found = self._find(node.left, name)
        if found is not None:
            return found
        return self._find(node.right, name)

    def insert(self, parent_name, child_name, side):
        """Add child_name under parent_name on 'left' or 'right'.
        Returns True on success, False if the insert was rejected."""
        if side not in ("left", "right"):
            print(f"Invalid side '{side}'. Use 'left' or 'right'.")
            return False

        parent = self._find(self.root, parent_name)
        if parent is None:
            print(f"Parent '{parent_name}' not found.")
            return False

        if getattr(parent, side) is not None:
            print(f"{parent_name} already has a {side} report.")
            return False

        setattr(parent, side, DoctorNode(child_name))
        return True

    def preorder(self, node):
        if node is None:
            return []
        return [node.name] + self.preorder(node.left) + self.preorder(node.right)

    def inorder(self, node):
        if node is None:
            return []
        return self.inorder(node.left) + [node.name] + self.inorder(node.right)

    def postorder(self, node):
        if node is None:
            return []
        return self.postorder(node.left) + self.postorder(node.right) + [node.name]


# Tests
tree = DoctorTree()
tree.root = DoctorNode("Dr. Croft")
tree.insert("Dr. Croft", "Dr. Goldsmith", "right")
tree.insert("Dr. Croft", "Dr. Phan", "left")
tree.insert("Dr. Phan", "Dr. Carson", "right")
tree.insert("Dr. Phan", "Dr. Morgan", "left")

print(tree.preorder(tree.root))
# ["Dr. Croft", "Dr. Phan", "Dr. Morgan", "Dr. Carson", "Dr. Goldsmith"]
print(tree.inorder(tree.root))
# ["Dr. Morgan", "Dr. Phan", "Dr. Carson", "Dr. Croft", "Dr. Goldsmith"]
print(tree.postorder(tree.root))
# ["Dr. Morgan", "Dr. Carson", "Dr. Phan", "Dr. Goldsmith", "Dr. Croft"]

# Edge cases
print(tree.insert("Dr. Nobody", "Dr. X", "left"))    # False: parent missing
print(tree.insert("Dr. Croft", "Dr. X", "middle"))   # False: invalid side
print(tree.insert("Dr. Croft", "Dr. X", "left"))     # False: slot already taken
print(DoctorTree().preorder(None))                   # [] : empty tree