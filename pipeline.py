import os
from dotenv import load_dotenv,find_dotenv
from pymongo import MongoClient

from kafka.consumer import consume_messages
from mongo import get_collection
from vector.embeddings import Sbert
from vector.models import Course, CourseRepo

load_dotenv(find_dotenv())

"""
Pipeline

A pipeline to get events from Kafka, vector embed using a simple sentence transformer and push to MongoDb

"""

consumer_config = {
    'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS'),
    'group.id': 'langchain-demo-local',
    'auto.offset.reset': 'earliest',
    'sasl.mechanism': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'enable.auto.commit': False,
    'sasl.username': os.getenv('KAFKA_USERNAME'),
    'sasl.password': os.getenv('KAFKA_PASSWORD')
}

sr_conf = {
    'url': os.getenv('SCHEMA_REGISTRY_URL'),
    'basic.auth.user.info': f"{os.getenv('SCHEMA_REGISTRY_USERNAME')}:{os.getenv('SCHEMA_REGISTRY_PASSWORD')}"
}

topics = ['coursev2']

mongo_user = os.getenv('MONGO_USER')
mongo_password = os.getenv('MONGO_PASSWORD')

courses_collection = get_collection(mongo_user, mongo_password, 'courses')
course_repo = CourseRepo(courses_collection)
model = Sbert()

def eventListener(event: Course):
    print(event)
    course_repo.save(event)

def dict_to_course(course_dict, ctx) -> Course:
    rows = []
    for k in sorted(course_dict.keys()):
        rows.append(f"{k}: {course_dict[k]}")
    text = "\n".join(rows)    
    embedddings = model.embed_query(text)

    return Course(
        id=course_dict.get('id'),
        title=course_dict.get('title', ''),
        subject=course_dict.get('subject'),
        content_embeddings=embedddings
    )

consume_messages(consumer_config, sr_conf, topics, eventListener, dict_to_course)

client.close()
