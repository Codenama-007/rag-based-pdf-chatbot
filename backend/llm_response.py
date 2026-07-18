from langchain_ollama import ChatOllama

llm = ChatOllama(
    model = 'phi4-mini-reasoning:latest' ,
    temperature = 0  
)

def generate_response_from_llm(top_chunks , user_query):
    
    prompt = f''' User has just provided us with the PDFs .
    just explain the content your response should not look like you are thinking but it should be more like a good explaination
    here are the top relevant chunks {top_chunks} and here is the User Query {user_query} 
    so now do the reasoning based on what chunks i have provided to you .
    when you will be doing the reasoning Tasks remeber that you dont mention what chunks just refer those chunks and explain the user query 
    '''
    
    Content = llm.invoke(prompt)
    
    return Content.content