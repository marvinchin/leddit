from models import Thread

"""
ThreadManager class stores threads and handles their ordering
Threads are stored in a list indexed by thread id
Ordering by rank is backed by a linked list data structure
"""
class ThreadManager:
    def __init__(self):
        self.threads = []   # init threads list
        self.nodes = {}     # init nodes dict mapping thread to rank node
        self.head = None    # init head of ranking linked list
        self.tail = None    # init tail of ranking linked list
        self.insertion = None   # init insertion point for new threads,
                                # should be the last node with least positive score
    """
    newThread creates a new thread with input topic
    """
    def newThread(self, topic):
        thread = Thread(len(self.threads), topic, 0)   # create the thread object
        self.threads.append(thread) # add it to threads list
        node = RankNode(thread.id, None, None)  # create generic RankNode
        self.nodes[thread.id] = node
        if self.head is None:
            # no other nodes in the list
            self.head = node
            self.tail = node
            self.insertion = node
        elif self.insertion is None:
            # all other nodes have negative score
            node.next = self.head
            self.head = node
            self.insertion = node
        else:
            # there are other nodes, insert behind node at insertion point
            self.insertion.insertAfter(node)
            if (self.insertion == self.tail):
                # insertion point is at the end of the list,
                # update tail to inserted node
                self.tail = node
            self.insertion = node

    """
    upvoteThread increases score of thread with input id and adjusts the ordering
    """
    def upvoteThread(self, threadId):
        thread = self.threads[threadId]
        thread.score += 1
        # update the linked list
        node = self.nodes[threadId]
        # check if node is the insertion point. Update if it is
        if self.insertion == node and node.prevNode is not None:
            self.insertion = node.prevNode

        # check if node is tail. Update if it is
        if self.tail == node and node.prevNode is not None:
            self.tail = node.prevNode

        if node == self.head:
            # already front of the list, no movement
            return
        else:
            considerNode = node.prevNode
            node.remove() # remove node from it's position from linked list
            considerThread = self.threads[considerNode.threadId]
            while considerThread.score <= thread.score:
                # final position of node is somewhere before this node
                if considerNode == self.head:
                    # at front of list, set node to head
                    node.nextNode = considerNode
                    considerNode.prevNode = node
                    self.head = node
                    # check if considerNode is the insertion point. Update if necessary
                    if (self.insertion is None and thread.score >= 0):
                        self.insertion = node
                    return
                else:
                    # repeat consideration with next previous node
                    considerNode = considerNode.prevNode
                    considerThread = self.threads[considerNode.threadId]

            # considerNode is the first node to the back of node's original
            # position with score higher than node. Final position is after this
            considerNode.insertAfter(node)
            # check if considerNode is insertion point. Update if necessary
            if self.insertion == considerNode and thread.score >= 0:
                self.insertion = node

            # check if considerNode is tail. Update if necessary
            if self.tail == considerNode:
                self.tail = node

    """
    downvoteThread decreases score of thread with input id and adjusts the ordering
    """
    def downvoteThread(self, threadId):
        thread = self.threads[threadId]
        thread.score -= 1
        # update the linked list
        node = self.nodes[threadId]
        # check if node is the insertion point. Update if score less than 0
        if self.insertion == node and thread.score < 0:
            if node.prevNode is not None:
                self.insertion = node.prevNode
            else:
                self.insertion = None

        #check if node is the head. Update if necessary
        if self.head == node and node.nextNode is not None:
            self.head = node.nextNode

        if node == self.tail:
            # already tail of the list, no movement
            return
        else:
            considerNode = node.nextNode
            node.remove() # remove node from it's position from linked list
            considerThread = self.threads[considerNode.threadId]
            while thread.score < considerThread.score:
                # final position of node is somewhere after this node
                if considerNode == self.tail:
                    # at back of list, set node to tail
                    node.prevNode = considerNode
                    considerNode.nextNode = node
                    self.tail = node
                    # check if considerNode is the insertion point. Update if necessary
                    if (self.insertion == considerNode and thread.score >= 0):
                        self.insertion = node
                    return
                else:
                    # repeat consideration with next previous node
                    considerNode = considerNode.nextNode
                    considerThread = self.threads[considerNode.threadId]

            # considerNode is the first node to the back of node's original
            # position with score higher than node. Final position is after this
            considerNode.insertBefore(node)
            # check if considerNode is insertion point. Update if necessary
            if (node.prevNode is not None and self.insertion == node.prevNode
                and thread.score >= 0):
                self.insertion = node

            #check if considerNode is the head. Update if necessary
            if self.head == considerNode:
                self.head = node

    """
    getThread returns the thread with input id
    """
    def getThread(self, threadId):
        return self.threads[threadId]


    """
    getThreads returns the list of threads of rank start(inclusive) to end(exclusive)
    ordered by rank
    """
    def getThreads(self, start, end):
        i = 0
        result = []
        currNode = self.head
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
