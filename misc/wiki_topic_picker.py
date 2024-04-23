import xml.etree.ElementTree as ET
import random
import os

class TopicPicker:
    def __init__(self, filepath, seed_value):
        self.filepath = filepath
        self.seed_value = seed_value
        self.create_topic_data_structure()

    def extract_topics(self):
        topics = []
        with open(os.path.join(self.filepath), 'r', encoding="utf-8") as file:
            for line in file:
                topic = line.strip()
                topics.append(topic)
        return topics

    def create_topic_data_structure(self):
        topics = self.extract_topics()
        topic_dict = {i: topic for i, topic in enumerate(topics)}
        return topic_dict

    def select_new_topic(self, topic_dict):
        random.seed(self.seed_value)
        random_topic_index = random.randint(0, len(topic_dict) - 1)
        random_topic = topic_dict[random_topic_index]
        return random_topic
