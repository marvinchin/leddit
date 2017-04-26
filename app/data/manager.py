from models import Thread

"""
ThreadManager class stores threads and handles their ordering
Threads are stored in a list indexed by thread id
Ordering by rank is backed by a linked list data structure
"""
class ThreadManager:
    def __init__(self):
        self.threads = []   # list containing thread objects
        self.nodes = {}     # dict mapping nodes to threads
        self.head = None    # points to the node of thread with highest score
        self.tail = None    # points to the node of thread with lowest score
        self.insertion = None   # points to the node which new threads should be
                                # inserted after, or none if new thread should
                                # be inserted as head.
                                # should be the last node with least non-negative score
    """
    newThread creates a new thread with input topic
    """
    def newThread(self, topic):
        # create new thread object and add it to the list
        thread = Thread(len(self.threads), topic, 0)
        self.threads.append(thread)
        # create generic RankNode to represent thread in the linked list, and
        # add it to the mapping dict
        node = RankNode(thread.id, None, None)
        self.nodes[thread.id] = node

        # if there is no head, then list is empty. insert node as first element
        if self.head is None:
            self.head = node
            self.tail = node
            self.insertion = node
        # if inesrtion is none, all other nodes have negative score.
        # insert node as first element and update insertion point to node
        elif self.insertion is None:
            node.next = self.head
            self.head = node
            self.insertion = node
        # other positive nodes exist. insert node behind insertion point and
        # update insertion point to node
        else:
            self.insertion.insertAfter(node)
            # if inserting after the last element, update tail to node
            if (self.insertion == self.tail):
                self.tail = node
            self.insertion = node

    """
    upvoteThread increases score of thread with input id and adjusts the ordering
    """
    def upvoteThread(self, threadId):
        self.checkValidId(threadId)
        thread = self.getThread(threadId)
        thread.score += 1
        # move the nodes to maintain ordering of threads
        node = self.nodes[threadId]

        # prepare for removal of node
        # if specified thread is insertion point, and it has a node before it
        # update insertion point to previous node
        if self.insertion == node and node.prevNode is not None:
            self.insertion = node.prevNode

        # if specified node is the head, there is no movement
        if node == self.head:
            return

        # if specified thread is tail, and it has a node before it, set tail
        # to previous node
        if self.tail == node and node.prevNode is not None:
            self.tail = node.prevNode

        # check potential nodes that may need to be moved, starting from the
        # node before specified node
        considerNode = node.prevNode
        considerThread = self.getThread(considerNode.threadId)
        # remove node from it's position from linked list
        node.remove()
        # search previous nodes until we find a node with score higher than
        # specified node
        while considerThread.score <= thread.score:
            # if node we are considering is already the head, specified thread
            # has the highest score and should be inserted as head
            if considerNode == self.head:
                node.nextNode = considerNode
                considerNode.prevNode = node
                self.head = node
                # if there are no non-negative nodes, and upvote makes this
                # thread's score non-negative, update insertion to this thread
                if (self.insertion is None and thread.score >= 0):
                    self.insertion = node
                return
            # continue consideration with previous node
            else:
                considerNode = considerNode.prevNode
                considerThread = self.getThread(considerNode.threadId)

        # considerNode now points to the first node ahead of specified node
        # with score greater than this node. Insert node behind considerNode
        considerNode.insertAfter(node)

        # if considerNode was the insertion point, and score of this thread is
        # non negative, then update insertion point to this node
        if self.insertion == considerNode and thread.score >= 0:
            self.insertion = node

        # if considerNode was the tail of the list, then update tail to this node
        if self.tail == considerNode:
            self.tail = node

    """
    downvoteThread decreases score of thread with input id and adjusts the ordering
    """
    def downvoteThread(self, threadId):
        self.checkValidId(threadId)
        thread = self.getThread(threadId)
        thread.score -= 1
        # move the nodes to maintain ordering of threads
        node = self.nodes[threadId]

        # prepare for removal of node
        # if specified node is the insertion point and thread score is negative,
        # we need to update insertion
        if self.insertion == node and thread.score < 0:
            # if there is a node before this, update insertion to previous node
            if node.prevNode is not None:
                self.insertion = node.prevNode
            # if there are no nodes before this, there are no more non-negative
            # nodes in the list. update insertion to none
            else:
                self.insertion = None

        # if specified node is the tail, there is no movement
        if node == self.tail:
            return

        # if specified node is the head, and there is a node after it, set head
        # to next node
        if self.head == node and node.nextNode is not None:
            self.head = node.nextNode

        # check potential nodes that may need to be moved, starting from the
        # node after specified node
        considerNode = node.nextNode
        considerThread = self.getThread(considerNode.threadId)
        node.remove()
        # search next nodes until we find a node with score lower than or equal
        # to specified node
        while thread.score < considerThread.score:
            # if node we are considering is already the tail, specified thread
            # has lowest score and should be inserted as tail
            if considerNode == self.tail:
                node.prevNode = considerNode
                considerNode.nextNode = node
                self.tail = node
                # if tail node is the insertion point, and thread score is non-
                # negative, update insertion point to node
                if (self.insertion == considerNode and thread.score >= 0):
                    self.insertion = node
                return
            # continue consideration with next node
            else:
                considerNode = considerNode.nextNode
                considerThread = self.getThread(considerNode.threadId)

        # considerNode now points to the first node behind specified node
        # with score smaller than or equal to this node. Insert node in front
        # of considerNode
        considerNode.insertBefore(node)

        # if node now has a node before it, and if that node is the insertion
        # point, and node has a non-negative score, it is now the smallest non-
        # negative scoring thread
        if (node.prevNode is not None and self.insertion == node.prevNode
            and thread.score >= 0):
            self.insertion = node

        # if considerNode was the head of the list, then update head to this node
        if self.head == considerNode:
            self.head = node

    """
    getThread returns the thread with input id
    """
    def getThread(self, threadId):
        self.checkValidId(threadId)
        return self.threads[threadId]


    """
    getThreads returns the list of threads of rank start(inclusive) to end(exclusive)
    ordered by rank
    """
    def getThreads(self, start, end):
        i = 0
        result = []
        currNode = self.head
        # iterate through nodes from 0 to end, or until no more nodes
        # if i is within range of start to end, then corresponding thread is
        # in the result set
        while (i < end and currNode is not None):
            if i >= start:
                result.append(self.getThread(currNode.threadId))
            i += 1
            currNode = currNode.nextNode
        return result

    """
    getAllThreads returns the list of all thread ids ordered by rank. Used for
    debugging purposes
    """
    def getAllThreadIds(self):
        result = []
        currNode = self.head
        while (currNode is not None):
            result.append(currNode.threadId)
            currNode = currNode.nextNode
        return result

    """
    checkValidId checks if the input threadId is valid. Raises Index Error if
    it is not
    """
    def checkValidId(self, threadId):
        numThreads = len(self.threads)
        if (threadId < 0 or threadId >= numThreads):
            raise IndexError('InvalidThreadId')


"""
RankNode class provides linked list functionality to back up the ordering of
threads by score
"""
class RankNode:
    def __init__(self, threadId, prevNode, nextNode):
        self.threadId = threadId
        self.prevNode = prevNode
        self.nextNode = nextNode

    """
    insertAfter inserts the given node into the list after itself
    """
    def insertAfter(self, newNode):
        nextNode = self.nextNode
        newNode.prevNode = self
        self.nextNode = newNode
        newNode.nextNode = nextNode
        if nextNode is not None:
            nextNode.prevNode = newNode

    """
    insertBefore inserts the given node into the list before itself
    """
    def insertBefore(self, newNode):
        prevNode = self.prevNode
        newNode.nextNode = self
        self.prevNode = newNode
        newNode.prevNode = prevNode
        if prevNode is not None:
            prevNode.nextNode = newNode

    """
    remove removes itself from the list
    """
    def remove(self):
        nextNode = self.nextNode
        prevNode = self.prevNode
        if nextNode is not None:
            nextNode.prevNode = prevNode
        if prevNode is not None:
            prevNode.nextNode = nextNode
        self.nextNode = None
        self.prevNode = None
