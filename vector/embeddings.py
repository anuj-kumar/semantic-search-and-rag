from langchain_huggingface import HuggingFaceEmbeddings

class Sbert(object):

    def __init__(self):
        self.model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def embed_query(self, text):
        return self.model.embed_query(text)