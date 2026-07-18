import numpy as np

def get_top_k_chunks(similarities , dataset , k = 7):
    results = []
    
    top_k_indices = np.argsort(similarities)[::-1][:k]
    for index in top_k_indices:
        results.append(
            {
                'chunks' : dataset.iloc[index]['Content']
            }
        )
    return results
    