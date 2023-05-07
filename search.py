import os
from dotenv import find_dotenv, load_dotenv
from mongo import get_collection
from vector import embeddings
from vector.models import CourseRepo

"""
Semantic search

CLI to semantic search text in the Mongo collection

"""


load_dotenv(find_dotenv())

model = embeddings.Sbert()

query = input("What would you like to search: ")

embedded = model.embed_query(query)

mongo_user = os.getenv('MONGO_USER')
mongo_password = os.getenv('MONGO_PASSWORD')

courses_collection = get_collection(mongo_user, mongo_password, 'courses')

course_repo = CourseRepo(courses_collection)
results = course_repo.semantic_search(embedded)
print(results)