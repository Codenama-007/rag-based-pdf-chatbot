from models.get_model import embedding_model

def generate_embeddings(text: str):

    embedding = embedding_model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()