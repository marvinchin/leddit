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


if __name__ == "__main__":
    unittest.main();
