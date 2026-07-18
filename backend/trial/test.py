import pymupdf4llm as llm
from langchain_ollama import ChatOllama
import ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter , MarkdownHeaderTextSplitter
import re
import pandas as pd 


print(" Lets get Started ")
# Embedding the Documents 
def embedding_the_content(content):
    embeddings = ollama.embed(
        model = 'bge-m3:latest' ,
        input = content
    )['embeddings'][0]
    
    return embeddings


# Cleaning of the Document 
def cleaning_of_the_document(document : str) -> str:
    # This is Replacing BR tags in the Content with Actual New Line Character 
    text = re.sub(r"<br\s*/?>" , "\n" , document , flags = re.IGNORECASE)
    
    # Stripping other Inline HTMl tags
    text = re.sub(r"<mark>(.*?)</mark>" , r"\1" , text , flags = re.IGNORECASE)
    text = re.sub(r"<(b|strong)>(.*?)</\1>" , r"\2" , text , flags = re.IGNORECASE)
    text = re.sub(r"<(i|em)>(.*?)</\1>" , r"\2" , text , flags = re.IGNORECASE)
    
    # Strip Any  HTML tags present 
    text = re.sub(r"<[^>]+>" , "" , text)
    
    # Collapse
    text = re.sub(r"\n{3 ,}" , "\n\n" , text)
    
    return text.strip()
     



# initializing Splitters 
headers_to_split = [
    ('#', 'h1'),
    ('##', 'h2'),
    ('###', 'h3')
]
mark_down_splitter = MarkdownHeaderTextSplitter(headers_to_split_on = headers_to_split , strip_headers = False)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 800 , 
    chunk_overlap = 120
)

# Begining with our task
document = llm.to_markdown("docs/PYTHON_PROGRAMMING_NOTES.pdf")
cleaned_document = cleaning_of_the_document(document)
header_chunks = mark_down_splitter.split_text(cleaned_document)
chunks = text_splitter.split_documents(header_chunks)

results = [
    
]

print(" And the main Process begins ")
for index , chunk in enumerate(chunks):
    results.append(
        {
            'source' : "python notes" ,
            'chunk' : chunk.page_content ,
            'embeddings' : embedding_the_content(chunk.page_content)
        }
    )

print(" Done With Embeddings ")
df = pd.DataFrame(results)
print(" Saving the File in the CSV format ")
print(df.tail())
print(df.info())
df.to_csv("trial.csv" , index = False)

print(" Done ")
print(" Ready for Further Tests ")
# while True:
#     user_query = input(" Ask Any Question You Want to ask ")
    
#     if 'quit' in user_query.lower() or 'bye' in user_query.lower():
#         break
    
    
    
    
# print(" Thank You for Using our Large Language Model ")