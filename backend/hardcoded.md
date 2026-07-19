useEffect(() => {
    const getProfile = async () => {
        const token = localStorage.getItem("token");
        const response = await fetch("http://127.0.0.1:8000/profile", {
            method: "GET",
            headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
            navigate('/');
            return;
        }

        const data = await response.json();
        setusername(data.username);
    };

    getProfile();
}, []);


# @app.post("/get-pdf")
# async def get_pdf(pdf: UploadFile = File(...),
#     token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_data_base),):
#     print(pdf.filename)
#     file = pdf.file
#     file_name = pdf.filename
    

#     with open(f"{FOLDER_NAME}/{file_name}" , 'wb') as file:
#         file.write(await pdf.read()) 
        
#     results = []
    
#     # Extracting the Content Related to the Document 
#     pdf_content = llm.to_markdown(f'{FOLDER_NAME}/{file_name}')
    
#     # Cleaning the content of pdf file 
    
#     cleaned_content = cleaning_of_the_document(pdf_content)
    
#     # Extracting the chunks from the cleaned content
    
#     chunks = chunking_the_file(cleaned_content)
#     for index , chunk in enumerate(chunks):
#         # print('-'*60)
#         # print(f" Chunk number -> {index + 1}")
#         # print(f" Chunk Metadat -> {chunk.metadata}")
#         # print(chunk.page_content)
#         # print(f'Total Words -> {len(chunk.page_content)}')
#         # print(f'Total Characters -> {len(chunk.page_content.split())}')
        
#         # Getting Embeddings for the File 
#         embeddings = generate_embeddings(chunk.page_content)
    
    
#         results.append({
#             'Source' : pdf.filename ,
#             'Content' : chunk.page_content ,
#             'embeddings' : embeddings
#         })
#     print(" Done with generating the dataset ")
#     df = pd.DataFrame(results)
    
#     print(" Saving the CSV file to Dataset Folder ")
#     df.to_csv(f"{DATASET_FOLDER_NAME}/{pdf.filename}.csv" , index = False)
#     print(" File Successfully saved to CSV data frame ")
#     return {
#         "status_code": 200,
#         "message": "File Reached the Backend Successfully and svaed to uploads folder currently its getting cleaned"
#     }