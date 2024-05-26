import os
from typing import Any
from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS

def run_llm(query:str)->Any:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    docsearch = FAISS.load_local('faiss_index_react', embeddings, allow_dangerous_deserialization=True)
    chat = GoogleGenerativeAI(model='gemini-pro', verbose=True, temperature=0)
    qa = RetrievalQA.from_llm(llm=chat, retriever=docsearch.as_retriever(), return_source_documents=True)
    return qa({"query": query})

if __name__ == '__main__':
    print(run_llm(query="What is RetrievalQA chain?"))