class LinkedList:
    def __init__(self):
        self.items = [] # list containing list objects
        self.nodes = {} # dict mapping list objects to nodes
        self.head = None # head points to object with highest score
        self.tail = None # tail points to object with lowest score
        self.insertion = None # insertion points to node that new objects should
                              # be inserted after

    """
    inserts the input item into the linked list, with a starting score of 0
    """
    def insert(self, newItem):
        id = len(self.items)
        item = ListItem(id, newItem)
        node = ListNode(item)
        self.items.append(item)
        self.nodes[id] = node

        # if head is None, then there are no nodes in the list
        if self.head is None:
            self.head = node
            self.tail = node
            self.insertion = node
        # if there are nodes in the list, but insertion is none, then there
        # are no positively scored nodes in the list
        elif self.insertion is None:
            # new node with score of 0 is the largest node, so insert before head
            self.head.insertBefore(node)
            # update head and insertion to point to this node
            self.head = node
            self.insertion = node
        else:
            self.insertion.insertAfter(node)
            # if insertion was tail, need to update tail to point to this node
            if self.insertion == self.tail:
                self.tail = node
            self.insertion = node

    """
    increases the score of the item with input item id by input amount
    """
    def incScore(self, id, amt):
        self.checkValidId(id)
        item = self.items[id]
        node = self.nodes[id]
        # if this node is the tail update it to point to previous node
        if self.tail == node:
            self.tail = node.prevNode
        # if this node is the insertion point update it to point to previous node
        # if there is no previous node, then this will still be the insertion point
        # after increasing score
        if self.insertion == node and node.prevNode is not None:
            self.insertion = node.prevNode

        # if this node is the head, no change in position
        if self.head == node:
            item.incScore(amt)
        # else we need to reinsert this node in the correct location
        else:
            item.incScore(amt)
            currNode = node.prevNode
            node.remove()
            while (currNode is not None and currNode.listItem.score < item.score):
                currNode = currNode.prevNode
            # if currNode is none, then there are no nodes with score larger than
            # the new score, so we insert it as the head of the list
            if currNode is None:
                self.head.insertBefore(node)
                self.head = node
            else:
                currNode.insertAfter(node)
                # if currNode is the tail, update it to point to this node
                if self.tail == currNode:
                    self.tail = node
                # if currNode is the insertion point, and this node has a
                # non-negative score, then update insertion point to point to
                # this node
                if self.insertion == currNode and item.score >= 0:
                    self.insertion = node

    """
    checks if the input item id is valid
    """
    def checkValidId(self, id):
        if id < 0 or id > len(self.items) - 1:
            raise IndexError("InvalidItemId")

"""
ListItem contains a reference to the item in the linked list, and maintains its score
"""
class ListItem:
    def __init__(self, id, item):
        self.id = id
        self.item = item
        self.score = 0

    def incScore(self, amt):
        self.score += amt

    def decScore(self, amt):
        self.score -= amt

"""
ListNode represents the position of a ListItem in the linked list
"""
class ListNode:
    def __init__(self, listItem):
        self.listItem = listItem
        self.prevNode = None
        self.nextNode = None

    """
    inserts the input node after this node in the linked list
    """
    def insertAfter(self, newNode):
        followingNode = self.nextNode
        self.nextNode = newNode
        newNode.prevNode = self
        newNode.nextNode = followingNode

        if followingNode is not None:
            followingNode.prevNode = newNode

    """
    inserts the input node before this node in the linked list
    """
    def insertBefore(self, newNode):
        previousNode = self.prevNode
        self.prevNode = newNode
        newNode.nextNode = self
        newNode.prevNode = previousNode
        if previousNode is not None:
            previousNode.nextNode = newNode

    """
    removes this node from the linked list
    """
    def remove(self):
        previousNode = self.prevNode
        followingNode = self.nextNode
        self.nextNode = None
        self.prevNode = None
        if previousNode is not None:
            previousNode.nextNode = followingNode
        if followingNode is not None:
            followingNode.prevNode = previousNode
