import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import ollama 
from langchain_ollama import ChatOllama
import numpy as np
import ast

# initializing the reasoning Model
llm = ChatOllama(model = 'qwen3:1.7b')


# Generating the Embeddings 
def generate_embeddings(content):
    embedding = ollama.embed(
        model = 'bge-m3:latest' ,
        input = content
    )['embeddings']
    
    return embedding

# Getting Top Relevant Chunks 
def get_top_k_chunks(similarities , dataset , k = 7):
    results = []
    
    top_k_indices = np.argsort(similarities)[::-1][:k]
    for index in top_k_indices:
        results.append(
            {
                'chunks' : dataset.iloc[index]['chunk']
            }
        )
    return results
    
    
def generate_response_from_llm(top_chunks , user_query):
    
    prompt = f''' User has just provided us with the PDFs .
    here are the top relevant chunks {top_chunks} and here is the User Query {user_query} 
    so now do the reasoning based on what chunks i have provided to you 
    '''
    
    Content = llm.invoke(prompt)
    
    return Content.content
    
    

# Loading the Dataset 
dataset = pd.read_csv('trial.csv')
# Convert stringified embeddings back into actual lists of floats
dataset['embeddings'] = dataset['embeddings'].apply(ast.literal_eval)

# Stack into a proper 2D numpy array (num_chunks x embedding_dim)
chunks_embeddings = np.vstack(dataset['embeddings'].to_numpy())

# generating an Infinite Loop 
while True:
    user_query = input(" Enter Your Query related to Python Programming Language \n ")
    
    if 'bye' in user_query.lower() or 'quit' in user_query.lower():
        break
    
    query_embedding =np.array(generate_embeddings(user_query)).reshape(1 , -1)
    similarities = cosine_similarity(
        query_embedding ,
        chunks_embeddings
    )[0]
    
    top_chunks = get_top_k_chunks(similarities , dataset)
    print(" Waiting for Response from LLM ")
    
    response = generate_response_from_llm(top_chunks , user_query)
    print(response)
    
    
    

print(" Thank you for using this RAG application ")
