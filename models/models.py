"""
Thread class encapsulates the information of each thread
"""
class Thread:
    def __init__(self, id, topic, score):
        if (len(topic) > 255):
            raise ValueError("Topic exceeds 255 characters")
        self.id = id
        self.topic = topic
        self.score = score

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

    def upvoteThread(self, threadId):
        thread = self.threads[threadId]
        thread.score += 1
        # update the linked list
        node = self.nodes[threadId]
        # check if node is the insertion point. Update if it is
        if self.insertion == node and node.prevNode is not None:
            self.insertion = node.prevNode

        if node == self.head:
            # already front of the list, no movement
            return
        else:
            considerNode = node.prevNode
            node.remove() # remove node from it's position from linked list
            considerThread = self.threads[considerNode.threadId]
            while considerThread.score < thread.score:
                # final position of node is somewhere before this node
                if considerNode == self.head:
                    # at front of list, set node to head
                    node.nextNode = considerNode
                    considerNode.prevNode = node
                    self.head = node
                    # check if head is the insertion point. Update if necessary
                    if (self.insertion == considerNode and thread.score >= 0):
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
            if (self.insertion == considerNode and thread.score >= 0):
                self.insertion = node


"""
RankNode class provides linked list functionality to back up the ordering of
threads by score
"""
class RankNode:
    def __init__(self, threadId, prevNode, nextNode):
        self.threadId = threadId
        self.prevNode = prevNode
        self.nextNode = nextNode

    def insertAfter(self, newNode):
        nextNode = self.nextNode
        newNode.prevNode = self
        self.nextNode = newNode
        newNode.nextNode = nextNode
        if nextNode is not None:
            nextNode.prevNode = newNode

    def remove(self):
        nextNode = self.nextNode
        prevNode = self.prevNode
        if nextNode is not None:
            nextNode.prevNode = prevNode
        if prevNode is not None:
            prevNode.nextNode = nextNode

    def toList(self):
        nodeList = []
        nodeList.append(self.threadId)
        if self.nextNode is None:
            return nodeList
        else:
            nextList = self.nextNode.toList()
            nodeList.extend(nextList)
            return nodeList
