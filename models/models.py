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
