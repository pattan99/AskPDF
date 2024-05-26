import os
from dotenv import load_dotenv

load_dotenv()

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

def store_pdf():
    pdf_path = 'uploaded_file.pdf'
    loader = PyPDFLoader(file_path=pdf_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=30, separator='\n')
    docs = text_splitter.split_documents(documents=documents)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    num_batch = 100
    vectorstore = FAISS.from_documents(docs[:num_batch], embeddings)
    for i in range(1, len(docs) // num_batch + 1):
        tmp = FAISS.from_documents(docs[num_batch * i:num_batch * (i + 1)], embeddings)
        vectorstore.merge_from(tmp)
    print(vectorstore.index.ntotal)
    vectorstore.save_local('faiss_index_react')