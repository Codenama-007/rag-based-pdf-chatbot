import numpy as np
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from Models import Users, Documents, DocumentChunks
from fastapi.middleware.cors import CORSMiddleware
from Schemas import User_Login, User_Create, QueryRequest
from Database import sessionlocal, engine, base
from sqlalchemy.orm import Session
import pymupdf4llm as llm
import os
import tempfile
from pdf_services.cleaning_document import cleaning_of_the_document
from pdf_services.file_chunking import chunking_the_file
from pdf_services.embeddings import generate_embeddings
from pdf_services.cloud_storage import upload_file_to_storage
from llm_response import generate_response_from_llm
from auth import hash_password, create_access_token, verify_password
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

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
    'http://localhost:5173',
    'localhost:5173' ,
    'https://rag-based-pdf-chatbot.netlify.app/'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


# Login Endpoint
@app.post("/login")
async def login(user: User_Login, db: Session = Depends(get_data_base)):
    db_user = db.query(Users).filter(Users.email == user.email).first()

    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email, "id": db_user.id})

    return {"access_token": token, "token_type": "bearer"}


# Registration Endpoint
@app.post("/register")
async def register(user: User_Create, db: Session = Depends(get_data_base)):
    existing_user = db.query(Users).filter(Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = Users(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"status_code": 200, "message": "Data stored in Database"}


# Endpoint for uploading + processing PDFs
@app.post("/get-pdf")
async def get_pdf(
    pdf: UploadFile = File(...),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_data_base),
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user = db.query(Users).filter(Users.email == payload.get("sub")).first()

    file_bytes = await pdf.read()
    storage_key = f"{user.id}/{pdf.filename}"
    upload_file_to_storage(file_bytes, storage_key)

    # Write to a real temp file, then close it BEFORE pymupdf opens it
    # (NamedTemporaryFile's default mode keeps the handle locked on Windows)
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".pdf")
    try:
        with os.fdopen(tmp_fd, "wb") as tmp:
            tmp.write(file_bytes)
        pdf_content = llm.to_markdown(tmp_path)
    finally:
        os.remove(tmp_path)

    cleaned_content = cleaning_of_the_document(pdf_content)
    chunks = chunking_the_file(cleaned_content)

    new_document = Documents(
        user_id=user.id,
        filename=pdf.filename,
        storage_key=storage_key,
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    for chunk in chunks:
        embedding = generate_embeddings(chunk.page_content)
        db_chunk = DocumentChunks(
            document_id=new_document.id,
            content=chunk.page_content,
            embedding=embedding,
        )
        db.add(db_chunk)

    db.commit()

    return {
        "status_code": 200,
        "message": "File uploaded and indexed",
        "document_id": new_document.id,
    }


# Profile Endpoint
@app.get("/profile")
async def profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_data_base)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")

    email = payload.get("sub")
    user = db.query(Users).filter(Users.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"username": user.username}


# Chat with a specific PDF
@app.post("/pdf-chat")
async def pdf_chatbot(
    text: QueryRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_data_base),
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user = db.query(Users).filter(Users.email == payload.get("sub")).first()

    document = db.query(Documents).filter(
        Documents.id == text.document_id,
        Documents.user_id == user.id
    ).first()

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    query_embedding = generate_embeddings(text.query)

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