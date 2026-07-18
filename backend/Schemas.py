from pydantic import BaseModel

class User_Login(BaseModel):
    email : str 
    password : str
    
class User_Create(BaseModel):
    username : str
    email : str
    password : str
    
class QueryRequest(BaseModel):
    query: str
