import ast
import numpy as np
from fastapi import FastAPI , UploadFile , File , Depends , HTTPException 
from Models import Users
from fastapi.middleware.cors import CORSMiddleware
from Schemas import User_Login , User_Create
from Database import sessionlocal , engine , base
from sqlalchemy.orm import Session
import pymupdf4llm as llm
import os 
import pandas as pd
from Schemas import QueryRequest
from pdf_services.cleaning_document import cleaning_of_the_document
from pdf_services.file_chunking import chunking_the_file
from pdf_services.embeddings import generate_embeddings
from sklearn.metrics.pairwise import cosine_similarity
from retrieve_chunks import get_top_k_chunks
from llm_response import generate_response_from_llm
from auth import hash_password , create_access_token , verify_password
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
from pdf_services.cloud_storage import upload_file_to_storage
from Models import Documents, DocumentChunks
import tempfile


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')

FOLDER_NAME = "uploads"
DATASET_FOLDER_NAME = "dataset"
os.makedirs(FOLDER_NAME , exist_ok = True)
os.makedirs(DATASET_FOLDER_NAME , exist_ok = True)



# Create tables automatically
base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get Database Session
def get_data_base():
    data_base = sessionlocal()
    
    try:
        yield data_base
    finally:
        data_base.close()



origins = [
    'http://localhost:5173' ,
    'localhost:5173'
]

app.add_middleware(
    CORSMiddleware ,
    allow_origins = origins ,
    allow_credentials = True ,
    allow_methods = ['*'] ,
    allow_headers = ['*']
)



# Creating a Login Endpoint 
@app.post("/login")
async def login(
    user: User_Login,
    db: Session = Depends(get_data_base)
):

    db_user = (
        db.query(Users)
        .filter(Users.email == user.email)
        .first()
    )

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "sub": db_user.email,
            "id": db_user.id
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
# Creating a Registeration Endpoint 
@app.post("/register")
async def register(user : User_Create , db: Session = Depends(get_data_base)):
    # Check if email exists
    existing_user = db.query(Users).filter(Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Store in database
    db_user = Users(
    username=user.username,
    email=user.email,
    password=hash_password(user.password)
)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(user.username)
    print(user.email)
    print(user.password)
    return {
        "status_code" : 200 ,
        "message" : "Data stored in Database"
    }




# generated from the claude side 
@app.post("/pdf-chat")
async def pdf_chatbot(
    text: QueryRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_data_base),
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user = db.query(Users).filter(Users.email == payload.get("sub")).first()

    # Make sure this document actually belongs to the logged-in user
    document = db.query(Documents).filter(
        Documents.id == text.document_id,
        Documents.user_id == user.id
    ).first()

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    query_embedding = generate_embeddings(text.query)

    # pgvector ranks chunks by cosine distance directly in the DB query
    top_chunks = (
        db.query(DocumentChunks)
        .filter(DocumentChunks.document_id == document.id)
        .order_by(DocumentChunks.embedding.cosine_distance(query_embedding))
        .limit(7)
        .all()
    )

    relevant_chunks = [{"chunks": chunk.content} for chunk in top_chunks]
    response = generate_response_from_llm(relevant_chunks, text.query)

    return {
        "status_code": 200,
        "response_from_llm": response,
        "message": "Request Reached the Backend Successfully"
    }
    
    
    
# Endpoint for getting the Profile Credentials 
@app.get("/profile")
async def profile(token : str = Depends(oauth2_scheme) , db:Session = Depends(get_data_base)):
    try:
        payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    except JWTError:
        raise HTTPException(
        status_code=401,
        detail="Invalid Token"
    )  
    
    email = payload.get("sub")
    
    user = db.query(Users).filter(
    Users.email == email
    ).first()

    if user is None:
        raise HTTPException(
        status_code=404,
        detail="User not found"
    )
# so i have to add this in my login endpoint
    
    return {
        "username" : user.username
    }

# Creating the Endpoint from where i will be receiving the PDF or word files 
@app.post("/pdf-chat")
async def pdf_chatbot(text : QueryRequest):
    print(text.query)
    
    user_query = text.query
    
    query_embedding = np.array(generate_embeddings(user_query)).reshape(1 , -1)
    print(len(query_embedding[0]))
    
    # Loading the Dataset 
    dataset = pd.read_csv(f'{DATASET_FOLDER_NAME}/MongoDB.pdf.csv')
    # Convert stringified embeddings back into actual lists of floats
    dataset['embeddings'] = dataset['embeddings'].apply(ast.literal_eval)

    # Stack into a proper 2D numpy array (num_chunks x embedding_dim)
    chunks_embeddings = np.vstack(dataset['embeddings'].to_numpy())
    print(len(chunks_embeddings[0]))
    
    similarities = cosine_similarity(chunks_embeddings, query_embedding).flatten()
    
    # Filename :- ReactJSNotesForProfessionals.pdf
    relevant_chunks = get_top_k_chunks(similarities , dataset)
    print(relevant_chunks)
    print(type(relevant_chunks))
    response = generate_response_from_llm(relevant_chunks , user_query)
    print(response)
    return {
        "status_code" : 200 ,
        "response_from_llm" : response ,
        "message" : "Request Reached the Backend Successfully"
    }
