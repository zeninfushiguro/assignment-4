class Patient:
    def __init__(self, name, urgency):
        if not isinstance(urgency, int) or not 1 <= urgency <= 10:
            raise ValueError("Urgency must be an integer from 1 to 10.")
        self.name = name
        self.urgency = urgency


class MinHeap:
    def __init__(self):
        self.data = []

    def heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.data[index].urgency < self.data[parent].urgency:
                self.data[index], self.data[parent] = self.data[parent], self.data[index]
                index = parent
            else:
                break

    def heapify_down(self, index):
        size = len(self.data)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < size and self.data[left].urgency < self.data[smallest].urgency:
                smallest = left
            if right < size and self.data[right].urgency < self.data[smallest].urgency:
                smallest = right

            if smallest == index:
                break
            self.data[index], self.data[smallest] = self.data[smallest], self.data[index]
            index = smallest

    def insert(self, patient):
        self.data.append(patient)
        self.heapify_up(len(self.data) - 1)

    def peek(self):
        if not self.data:
            return None
        return self.data[0]

    def remove_min(self):
        if not self.data:
            return None
        if len(self.data) == 1:
            return self.data.pop()
        root = self.data[0]
        self.data[0] = self.data.pop()
        self.heapify_down(0)
        return root

    def print_heap(self):
        print("Current Queue:")
        for p in self.data:
            print(f"- {p.name} ({p.urgency})")


# Tests
heap = MinHeap()
heap.insert(Patient("Jordan", 3))
heap.insert(Patient("Taylor", 1))
heap.insert(Patient("Avery", 5))
heap.print_heap()

next_up = heap.peek()
print(next_up.name, next_up.urgency)   # Taylor 1

served = heap.remove_min()
print(served.name)                     # Taylor
heap.print_heap()

# Edge cases
empty = MinHeap()
print(empty.peek())                    # None
print(empty.remove_min())              # None

one = MinHeap()
one.insert(Patient("Solo", 4))
print(one.remove_min().name)           # Solo
print(one.data)                        # []

ties = MinHeap()
for n, u in [("A", 2), ("B", 2), ("C", 1), ("D", 2)]:
    ties.insert(Patient(n, u))
print([ties.remove_min().name for _ in range(4)])   # C first, then the 2s

try:
    Patient("Bad", 11)
except ValueError as e:
    print(e)

#Design Memo
#A tree fits the doctor structure because the hospital's management is hierarchical: each doctor has a supervisor above them and up to two direct reports below. A binary tree models that one-to-many relationship directly, and because every subtree is itself a tree, recursive methods can process any branch with the same logic and a simple base case of reaching None.
#Traversal choice depends on what the task needs. Preorder visits a parent before its reports, which suits copying a tree or printing an org chart from the top down. Inorder visits the left subtree, the node, then the right subtree; on a binary search tree it returns values in sorted order. Postorder visits children before parents, which suits work that depends on reports being finished first, such as totaling workloads up the hierarchy or safely deleting a tree from the leaves up.
#Heaps help simulate real-time emergency intake because arrival order does not decide who is seen next; urgency does. A min-heap keeps the most urgent patient at index 0, so peek is O(1), while insert and remove_min only need to repair one path through the tree, which is O(log n). That is much cheaper than re-sorting the whole list after every arrival or discharge. The heap does not fully sort the queue, only guarantees the top element, which is exactly what intake needs. One limitation is that equal urgency patients are not guaranteed to be served in arrival order, so a real system would add a timestamp as a tie-breaker.
