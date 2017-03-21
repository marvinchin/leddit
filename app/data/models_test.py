import models
import manager
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

class ThreadthreadManagerTest(unittest.TestCase):
    def testCreate(self):
        threadManager = manager.ThreadManager()
        self.assertEqual(threadManager.threads, [])
        self.assertEqual(threadManager.nodes, {})
        self.assertEqual(threadManager.head, None)
        self.assertEqual(threadManager.tail, None)
        self.assertEqual(threadManager.insertion, None)

    def testNewThread(self):
        threadManager = manager.ThreadManager()
        threadManager.newThread("Hello")
        self.assertEqual(threadManager.threads[0].topic, "Hello")
        self.assertEqual(threadManager.nodes[0].threadId, 0)
        self.assertEqual(threadManager.head.threadId, 0)
        self.assertEqual(threadManager.tail.threadId, 0)
        self.assertEqual(threadManager.insertion.threadId, 0)
        threadManager.newThread("World")
        self.assertEqual(threadManager.threads[1].topic, "World")
        self.assertEqual(threadManager.nodes[1].threadId, 1)
        self.assertEqual(threadManager.head.threadId, 0)
        self.assertEqual(threadManager.tail.threadId, 1)
        self.assertEqual(threadManager.insertion.threadId, 1)

    def testUpvote(self):
        threadManager = manager.ThreadManager()
        threadManager.newThread("Three")  #id 0
        threadManager.newThread("Little") #id 1
        threadManager.newThread("Pigs")   #id 2
        threadManager.upvoteThread(2)
        self.assertEqual(threadManager.getAllThreadIds(), [2, 0, 1])
        threadManager.upvoteThread(2)
        self.assertEqual(threadManager.getAllThreadIds(), [2, 0, 1])
        threadManager.newThread("Oink")   #id 3
        self.assertEqual(threadManager.getAllThreadIds(), [2, 0, 1, 3])
        threadManager.upvoteThread(3)
        self.assertEqual(threadManager.getAllThreadIds(), [2, 3, 0, 1])
        threadManager.upvoteThread(3)
        self.assertEqual(threadManager.getAllThreadIds(), [3, 2, 0, 1])
        threadManager.upvoteThread(3)
        self.assertEqual(threadManager.getAllThreadIds(), [3, 2, 0, 1])
        self.assertEqual(threadManager.threads[3].score, 3)

    def testDownvote(self):
        threadManager = manager.ThreadManager()
        threadManager.newThread("Three")  #id 0
        threadManager.newThread("Little") #id 1
        threadManager.newThread("Pigs")   #id 2
        threadManager.downvoteThread(2)
        self.assertEqual(threadManager.getAllThreadIds(), [0, 1, 2])
        self.assertEqual(threadManager.insertion.threadId, 1)
        threadManager.newThread("Oink")   #id 3
        self.assertEqual(threadManager.getAllThreadIds(), [0, 1, 3, 2])
        threadManager.downvoteThread(1)
        self.assertEqual(threadManager.getAllThreadIds(), [0, 3, 1, 2])
        threadManager.downvoteThread(1)
        self.assertEqual(threadManager.getAllThreadIds(), [0, 3, 2, 1])
        self.assertEqual(threadManager.threads[1].score, -2)
        threadManager.upvoteThread(3)
        threadManager.upvoteThread(0)
        self.assertEqual(threadManager.getAllThreadIds(), [0, 3, 2, 1])
        self.assertEqual(threadManager.insertion.threadId, 3)
        threadManager.upvoteThread(2)
        self.assertEqual(threadManager.getAllThreadIds(), [0, 3, 2, 1])
        self.assertEqual(threadManager.insertion.threadId, 2)

    def testGetThreads(self):
        threadManager = manager.ThreadManager()
        threadManager.newThread("Three")  #id 0
        threadManager.newThread("Little") #id 1
        threadManager.newThread("Pigs")   #id 2
        threadManager.newThread("Oink")   #id 3
        threads = threadManager.getThreads(1, 3)
        ids = []
        for t in threads:
            ids.append(t.id)
        self.assertEqual(ids, [1, 2])
        threadManager.upvoteThread(3)
        threads = threadManager.getThreads(1, 4)
        ids = []
        for t in threads:
            ids.append(t.id)
        self.assertEqual(ids, [0, 1, 2])



if __name__ == "__main__":
    unittest.main();
