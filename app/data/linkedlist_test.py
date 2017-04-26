from linkedlist import LinkedList, ListItem, ListNode
import unittest

class ListItemTest(unittest.TestCase):
    def test_create(self):
        item = "Test String"
        listItem = ListItem(0, item)
        self.assertEqual(listItem.id, 0)
        self.assertEqual(listItem.item, item)
        self.assertEqual(listItem.score, 0)

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


if __name__ == "__main__":
    unittest.main()
