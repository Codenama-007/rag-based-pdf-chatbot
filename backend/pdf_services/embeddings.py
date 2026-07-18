import ollama 

def generate_embeddings(content):
    embedding = ollama.embed(
        model = 'bge-m3:latest' ,
        input = content
    )['embeddings']
    
    return embedding