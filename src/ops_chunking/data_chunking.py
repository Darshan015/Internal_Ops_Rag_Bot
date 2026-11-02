from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()
from src.ops_ingestion.data_loader import document_load
from pathlib import Path

data_dir = Path(__file__).resolve().parents[2] / "data"

def split_document():
    loaded_doc = document_load(data_dir)
    #print("loaded_doc in chuncking",loaded_doc)
    if not loaded_doc:
        raise FileNotFoundError("No file loaded to split the documents")

    splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    doc_split = splitter.split_documents(documents=loaded_doc)
    # print("splitted_doc_len",len(doc_split))
    #print("splitted_doc_pagecontent",doc_split[600].page_content)
    #print("splitted_doc_metadata",doc_split[600].metadata)
    return doc_split

#split_document()
