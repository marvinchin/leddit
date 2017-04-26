class LinkedList:
    def __init__(self):
        self.items = [] # list containing list objects
        self.nodes = {} # dict mapping list objects to nodes
        self.head = None # head points to object with highest score
        self.tail = None # tail points to object with lowest score
        self.insertion = None # insertion points to node that new objects should
                              # be inserted after

    def insert(self, newItem):
        id = len(self.items)
        item = ListItem(id, newItem)
        node = ListNode(item)

        self.items.append(item)
        self.nodes[id] = node


class ListItem:
    def __init__(self, id, item):
        self.id = id
        self.item = item
        self.score = 0

class ListNode:
    def __init__(self, listItem):
        self.listItem = listItem
        self.prevNode = None
        self.nextNode = None

    def insertAfter(self, newNode):
        followingNode = self.nextNode
        self.nextNode = newNode
        newNode.prevNode = self
        newNode.nextNode = followingNode

        if followingNode is not None:
            followingNode.prevNode = newNode

    def insertBefore(self, newNode):
        previousNode = self.prevNode
        self.prevNode = newNode
        newNode.nextNode = self
        newNode.prevNode = previousNode
        if previousNode is not None:
            previousNode.nextNode = newNode

    def remove(self):
        previousNode = self.prevNode
        followingNode = self.nextNode
        self.nextNode = None
        self.prevNode = None
        if previousNode is not None:
            previousNode.nextNode = followingNode
        if followingNode is not None:
            followingNode.prevNode = previousNode
