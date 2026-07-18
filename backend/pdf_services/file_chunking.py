from langchain_text_splitters import MarkdownHeaderTextSplitter , RecursiveCharacterTextSplitter



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