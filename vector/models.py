from dataclasses import dataclass
from enum import Enum
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List

# Enum for subject
class Subject(Enum):
    PHY = "PHY"
    MATH = "MATH"
    ENG = "ENG"

    @staticmethod
    def from_string(subject_str: str):
        try:
            return Subject[subject_str]
        except KeyError:
            raise ValueError(f"Unknown subject: {subject_str}")

# Model class
class Course(object):
    id: int
    title: str
    subject: Subject
    content_embeddings: List[float]

    def __init__(self, id, title, subject, content_embeddings):
        self.id = id
        self.title = title
        self.subject = Subject.from_string(subject)
        self.content_embeddings = content_embeddings

# MongoDB client setup
# Function to save course embeddings
class CourseRepo:
    collection = None

    min_match_score = 0.5

    def __init__(self, collection):
        self.collection = collection

    def save(self, course: Course):
        course_dict = vars(course)
        course_dict['subject'] = course_dict['subject'].value  # Convert enum to string
        self.collection.insert_one(course_dict)

    def semantic_search(self, query_vector: List[float]):
        results = self.collection.aggregate([
            {
                "$vectorSearch": {
                    "index": "content_embeddings_vector",
                    "path": "content_embeddings",
                    "queryVector": query_vector,
                    "numCandidates": 100,
                    "limit": 10
                }
            },
            {
                "$project": {
                    "id": 1,
                    "title": 1,
                    "subject": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            },
            {
            "$match": {
                "score": {"$gt": self.min_match_score}  # Filter by minimum score
            }
        },
        ])
        return list(results)