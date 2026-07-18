# import pymupdf4llm as llm
# from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
# import json

# # Step 1 :- Extracting the Content From the Document 
# document = llm.to_markdown("docs/MongoDB.pdf")

# # Step 2 :- Performing Mark Down Splitting
# headers_to_split_on = [
#     ('#', 'h1'),
#     ('##', 'h2'),
#     ('###', 'h3')
# ]
# md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)
# header_chunks = md_splitter.split_text(document)   # returns list[Document]

# # Step 3 :- Performing Recursive Character Splitting 
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=800,
#     chunk_overlap=120
# )

# chunks = text_splitter.split_documents(header_chunks)   # <-- fixed: split_documents, not split_text

# results = []

# for index, chunk in enumerate(chunks):
#     print('-'*60)
#     print(f" Chunk Number {index} ")
#     print(f" Chunk {index} | metadata : {chunk.metadata}")
#     print(chunk.page_content)
#     print(f" Chars: {len(chunk.page_content)} | Words: {len(chunk.page_content.split())}")
#     print("="*60)
#     chunk.page_content.replace('\n' , ' ')
    
#     results.append(
#         {
#             "Chunk" : index ,
#             "metadata" : chunk.metadata ,
#             "content" : chunk.page_content ,
#         }
#     )
    
# print(" Converting all the Stuff into a JSON file ")
# # json.dump(results , 'json_file.json')
# with open("json_file.json" , 'w' , encoding = 'utf-8') as file:
#     json.dump(results , file  , indent = 2 , ensure_ascii = True )

import os
import pymupdf4llm as llm
from langchain_text_splitters import RecursiveCharacterTextSplitter , MarkdownHeaderTextSplitter
import time 
import re
import pandas as pd


results = []
# Step 1 :- Loading the Documents 
# Step 2 :- Chunking the Required Documents 
# Step 3 :- Saving the Chunks in a JSON File 


# Complementary Step :- Cleaning of the Document 

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
     

# Step 1 👇
def load_document(file):
    markdown_content = llm.to_markdown(f'docs/{file}')
    
    return markdown_content 

# Step 2 👇
def chunking_the_file(content):
    headers_to_split_on = [
    ('#', 'h1'),
    ('##', 'h2'),
    ('###', 'h3')
]
    # Initiallizing the Splitters 
    
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on = headers_to_split_on , strip_headers = False)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800 , 
        chunk_overlap = 120 
    )


    # performing the MarkDown Splitting 
    header_chunks = markdown_splitter.split_text(content)
    
    # Performing Character Text Splitting 
    chunks = text_splitter.split_documents(header_chunks)
    
    return chunks 



docs_folder = os.listdir('docs')

for pdf_file in docs_folder:
    print(" Loading the Content of the file ",pdf_file)
    
    # Loading the Content of file 
    file_content = load_document(pdf_file)
    
    # Cleaning the Document Content 
    cleaned_content = cleaning_of_the_document(file_content)
    
    # Chunking the File Content
    chunks = chunking_the_file(cleaned_content)
    
    # Step 3 👇
    for index , chunk in enumerate(chunks):
        print("="*60)
        print(f" Chunk Number {index} ")
        print(f" Chunk {index} metadata {chunk.metadata} ")
        print(chunk.page_content)
        print(f" Total Words {len((chunk.page_content).split())} ")
        print(f" Total Characters {len(chunk.page_content)} ")
        
        results.append(
            {
                'Source' : pdf_file ,
                'Chunk Metadata' : chunk.metadata ,
                'Content' : chunk.page_content 
            }
        )
    
    # Gettting a json file of the chunks obtained 
    # json_file = returning_json_file_of_chunks(chunks)
    
    time.sleep(3)
    
df = pd.DataFrame(results)

print(df.info)
print(df.head())
print(df.tail())
print(" Saving the Dataframe as a CSV file ")
df.to_csv("dataset.csv" , index = False)