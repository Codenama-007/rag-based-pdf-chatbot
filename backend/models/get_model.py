import os
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(
    os.getenv("EMBEDDING_MODEL")
)