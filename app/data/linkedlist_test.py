from linkedlist import LinkedList, ListItem, ListNode
import unittest

class ListItemTest(unittest.TestCase):
    def test_create(self):
        item = "Test String"
        listItem = ListItem(0, item)
        self.assertEqual(listItem.id, 0)
        self.assertEqual(listItem.item, item)
        self.assertEqual(listItem.score, 0)

    def test_inc_score(self):
        item = "Test String"
        listItem = ListItem(0, item)
        listItem.incScore(5)
        self.assertEqual(listItem.score, 5)

    def test_dec_score(self):
        item = "Test String"
        listItem = ListItem(0, item)
        listItem.decScore(5)
        self.assertEqual(listItem.score, -5)

class ListNodeTest(unittest.TestCase):
    def test_create(self):
        listItem = ListItem(0, "Hello")
        node = ListNode(listItem)
        self.assertEqual(node.listItem, listItem)
        self.assertEqual(node.nextNode, None)
        self.assertEqual(node.prevNode, None)

    def test_insert_after_single(self):
        firstItem = ListItem(0, "First")
        firstNode = ListNode(firstItem)
        insertItem = ListItem(1, "Insert")
        insertNode = ListNode(insertItem)
        firstNode.insertAfter(insertNode)
        self.assertEqual(firstNode.prevNode, None)
        self.assertEqual(firstNode.nextNode, insertNode)
        self.assertEqual(insertNode.prevNode, firstNode)
        self.assertEqual(insertNode.nextNode, None)

    def test_insert_after_between_nodes(self):
        firstItem = ListItem(0, "First")
        firstNode = ListNode(firstItem)
        secondItem = ListItem(1, "Second")
        secondNode = ListNode(secondItem)
        insertItem = ListItem(2, "Insert")
        insertNode = ListNode(insertItem)
        firstNode.insertAfter(secondNode)
        firstNode.insertAfter(insertNode)
        self.assertEqual(firstNode.nextNode, insertNode)
        self.assertEqual(insertNode.prevNode, firstNode)
        self.assertEqual(insertNode.nextNode, secondNode)
        self.assertEqual(secondNode.prevNode, insertNode)

    def test_insert_before_single(self):
        firstItem = ListItem(0, "First")
        firstNode = ListNode(firstItem)
        insertItem = ListItem(1, "Insert")
        insertNode = ListNode(insertItem)
        firstNode.insertBefore(insertNode)
        self.assertEquals(firstNode.prevNode, insertNode)
        self.assertEquals(firstNode.nextNode, None)
        self.assertEquals(insertNode.nextNode, firstNode)
        self.assertEquals(insertNode.prevNode, None)

    def test_insert_before_between_nodes(self):
        firstItem = ListItem(0, "First")
        firstNode = ListNode(firstItem)
        secondItem = ListItem(1, "Second")
        secondNode = ListNode(secondItem)
        insertItem = ListItem(2, "Insert")
        insertNode = ListNode(insertItem)
        firstNode.insertAfter(secondNode)
        secondNode.insertBefore(insertNode)
        self.assertEquals(firstNode.nextNode, insertNode)
        self.assertEquals(insertNode.prevNode, firstNode)
        self.assertEquals(insertNode.nextNode, secondNode)
        self.assertEquals(secondNode.prevNode, insertNode)

    def test_remove_single_node(self):
        firstItem = ListItem(0, "First")
        firstNode = ListNode(firstItem)
        removeItem = ListItem(1, "Remove")
        removeNode = ListNode(removeItem)
        firstNode.insertAfter(removeNode)
        removeNode.remove()
        self.assertEquals(firstNode.nextNode, None)
        self.assertEquals(removeNode.prevNode, None)
        self.assertEquals(removeNode.nextNode, None)
        removeNode.insertAfter(firstNode)
        removeNode.remove()
        self.assertEquals(firstNode.prevNode, None)
        self.assertEquals(removeNode.prevNode, None)
        self.assertEquals(removeNode.nextNode, None)

    def test_remove_between_nodes(self):
        firstItem = ListItem(0, "First")
        firstNode = ListNode(firstItem)
        secondItem = ListItem(1, "Second")
        secondNode = ListNode(secondItem)
        removeItem = ListItem(2, "Insert")
        removeNode = ListNode(removeItem)
        firstNode.insertAfter(removeNode)
        removeNode.insertAfter(secondNode)
        removeNode.remove()
        self.assertEquals(firstNode.nextNode, secondNode)
        self.assertEquals(secondNode.prevNode, firstNode)
        self.assertEquals(removeNode.nextNode, None)
        self.assertEquals(removeNode.prevNode, None)

class LinkedListTest(unittest.TestCase):
    def test_insert_empty(self):
        linkedlist = LinkedList()
        firstItem = "First Insert"
        linkedlist.insert(firstItem)
        self.assertEquals(linkedlist.items[0].item, firstItem)
        firstNode = linkedlist.nodes[0]
        self.assertEquals(firstNode.listItem.item, firstItem)
        self.assertEquals(linkedlist.head, firstNode)
        self.assertEquals(linkedlist.tail, firstNode)
        self.assertEquals(linkedlist.insertion, firstNode)
        secondItem = "Second Insert"
        linkedlist.insert(secondItem)
        secondNode = linkedlist.nodes[1]
        self.assertEquals(linkedlist.head, firstNode)
        self.assertEquals(linkedlist.tail, secondNode)
        self.assertEquals(linkedlist.insertion, secondNode)

    def test_insert_all_negative(self):
        linkedlist = LinkedList()
        firstItem = "First Insert"
        linkedlist.insert(firstItem)
        firstNode = linkedlist.nodes[0]
        firstListItem = linkedlist.items[0]
        firstListItem.score = -1 # set score to negative, so there are no
                                 # positively scored items
        linkedlist.insertion = None # set insertion pointer to None
        secondItem = "Second Insert"
        linkedlist.insert(secondItem)
        secondNode = linkedlist.nodes[1]
        self.assertEquals(linkedlist.head, secondNode)
        self.assertEquals(linkedlist.insertion, secondNode)
        self.assertEquals(linkedlist.tail, firstNode)

    def test_inc_score_invalid(self):
        linkedlist = LinkedList()
        with self.assertRaises(IndexError):
            linkedlist.incScore(0, 1)

    def test_inc_score_all_positive(self):
        linkedlist = LinkedList()
        firstItem = "First Insert"
        linkedlist.insert(firstItem)
        firstNode = linkedlist.nodes[0]
        secondItem = "Second Insert"
        linkedlist.insert(secondItem)
        secondNode = linkedlist.nodes[1]
        thirdItem = "Third Insert"
        linkedlist.insert(thirdItem)
        thirdNode = linkedlist.nodes[2]
        linkedlist.incScore(1, 1) # increase the second item score by 1
        self.assertEquals(linkedlist.head, secondNode)
        self.assertEquals(linkedlist.tail, thirdNode)
        self.assertEqual(linkedlist.insertion, thirdNode)
        linkedlist.incScore(2, 1) # increase the third item score by 1
        self.assertEqual(linkedlist.head, secondNode)
        self.assertEqual(linkedlist.tail, firstNode)
        self.assertEqual(linkedlist.insertion, firstNode)

    def test_inc_score_all_positive(self):
        linkedlist = LinkedList()
        firstItem = "First Insert"
        linkedlist.insert(firstItem)
        firstNode = linkedlist.nodes[0]
        secondItem = "Second Insert"
        linkedlist.insert(secondItem)
        secondNode = linkedlist.nodes[1]
        thirdItem = "Third Insert"
        linkedlist.insert(thirdItem)
        thirdNode = linkedlist.nodes[2]
        # set second node score to -1, third node score to -2
        secondNode.listItem.score = -1
        thirdNode.listItem.score = -2
        linkedlist.insertion = firstNode
        linkedlist.incScore(0, 1) # increase first item score by 1
        self.assertEquals(linkedlist.head, firstNode)
        self.assertEquals(linkedlist.tail, thirdNode)
        self.assertEquals(linkedlist.insertion, firstNode)
        linkedlist.incScore(2, 1) # increase third item score by 1
        # ordering should remain unchanged
        self.assertEquals(linkedlist.head, firstNode)
        self.assertEquals(linkedlist.tail, thirdNode)
        self.assertEquals(linkedlist.insertion, firstNode)
        linkedlist.incScore(1, 1) # increase the second item score by 1
        # score becomes 0, ordering remain unchanged but insertion should be
        # set to second node
        self.assertEquals(linkedlist.head, firstNode)
        self.assertEquals(linkedlist.tail, thirdNode)
        self.assertEquals(linkedlist.insertion, secondNode)
        linkedlist.incScore(2, 1) # increase the third item score by 1
        # score becomes 0, ordering remain unchanged but insertion should be
        # set to third node
        self.assertEquals(linkedlist.head, firstNode)
        self.assertEquals(linkedlist.tail, thirdNode)
        self.assertEquals(linkedlist.insertion, thirdNode)

if __name__ == "__main__":
    unittest.main()
