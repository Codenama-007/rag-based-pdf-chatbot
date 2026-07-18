import re
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
     