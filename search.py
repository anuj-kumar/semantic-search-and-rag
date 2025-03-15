import os
from dotenv import find_dotenv, load_dotenv
from mongo import get_collection
from vector import embeddings
from vector.models import CourseRepo
import google.generativeai as genai


"""
Semantic search

CLI to semantic search text in the Mongo collection

"""


load_dotenv(find_dotenv())

def generate_answer(prompt):
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("Gemini API Key not provided. Please provide GEMINI_API_KEY as an environment variable")
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    answer = model.generate_content(prompt)
    return answer.text

model = embeddings.Sbert()

query = input("What would you like to search: ")

embedded = model.embed_query(query)

mongo_user = os.getenv('MONGO_USER')
mongo_password = os.getenv('MONGO_PASSWORD')

courses_collection = get_collection(mongo_user, mongo_password, 'courses')

course_repo = CourseRepo(courses_collection)
results = course_repo.semantic_search(embedded)
# print(results)


prompt = ("""You are a course search assistant. You will find the most relevant courses for the given query using the context given in a structured format.
          Query: '{query}'
          context: '{context}'
          """).format(query=query, context=results)

print(generate_answer(prompt))

# messages = [system_prompt, query, results]

# client = OpenAI()

# completions = client.chat.completions.create(
#     model="gpt-4o mini",
#     messages=[
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": query},
#         {"role": "assistant", "content": str(results)}
#     ]
# )
# print(completions.model_dump())

