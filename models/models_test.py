import models
import unittest

class ThreadTest(unittest.TestCase):
    def testCreate(self):
        thread = models.Thread(0, "Hello World", 0)
        self.assertEqual(thread.id, 0)
        self.assertEqual(thread.topic, "Hello World")
        self.assertEqual(thread.score, 0)

    def testExceedLength(self):
        topic = "G9MzsU5smW5s619VrQyUSFV38o57PhDkRD5hxVQYbcmy4kvBuBpENbHq8gGfH8QWSgxHKf1LpE5vZ7Lm527ICkhMqiOuukP1CcU0GfZ1tgJpyWbqXgFB0jO4srcRzTypSgkiIO1FPhpZfz9Cevqwc3cTe0Yvpml8raDoUBEx5elaxkOzRDOmIXZaGmeMz2gHIsGN9uJ4sOEtTTMgVtxhGtYBnnk9shR5QNwfNsBOzhsQfVXzWig1Snb7eD0XWF7H"
        with self.assertRaises(ValueError):
            thread = models.Thread(0, topic, 0)

class ThreadManagerTest(unittest.TestCase):
    def testCreate(self):
        manager = models.ThreadManager()
        self.assertEqual(manager.threads, [])
        self.assertEqual(manager.nodes, {})
        self.assertEqual(manager.head, None)
        self.assertEqual(manager.tail, None)
        self.assertEqual(manager.insertion, None)

    def testNewThread(self):
        manager = models.ThreadManager()
        manager.newThread("Hello")
        self.assertEqual(manager.threads[0].topic, "Hello")
        self.assertEqual(manager.nodes[0].threadId, 0)
        self.assertEqual(manager.head.threadId, 0)
        self.assertEqual(manager.tail.threadId, 0)
        self.assertEqual(manager.insertion.threadId, 0)
        manager.newThread("World")
        self.assertEqual(manager.threads[1].topic, "World")
        self.assertEqual(manager.nodes[1].threadId, 1)
        self.assertEqual(manager.head.threadId, 0)
        self.assertEqual(manager.tail.threadId, 1)
        self.assertEqual(manager.insertion.threadId, 1)

    def testUpvote(self):
        manager = models.ThreadManager()
        manager.newThread("Three")  #id 0
        manager.newThread("Little") #id 1
        manager.newThread("Pigs")   #id 2
        manager.upvoteThread(2)
        self.assertEqual(manager.head.toList(), [2, 0, 1])
        manager.upvoteThread(2)
        self.assertEqual(manager.head.toList(), [2, 0, 1])
        manager.newThread("Oink")   #id 3
        self.assertEqual(manager.head.toList(), [2, 0, 1, 3])
        manager.upvoteThread(3)
        self.assertEqual(manager.head.toList(), [2, 3, 0, 1])
        manager.upvoteThread(3)
        self.assertEqual(manager.head.toList(), [2, 3, 0, 1])
        manager.upvoteThread(3)
        self.assertEqual(manager.head.toList(), [3, 2, 0, 1])
        self.assertEqual(manager.threads[3].score, 3)

if __name__ == "__main__":
    unittest.main();
