from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader,PyPDFDirectoryLoader

data_dir = Path(__file__).resolve().parents[2] / "data"

def document_load(path:str):
   # print("path:",path)
   directory = Path(path)
  # print("dir",directory)
   if not directory.exists():
    raise FileNotFoundError(f"Directory Not Foud {path}")  

   loader = PyPDFDirectoryLoader(path=str(directory))
   doc_loaded = loader.load()
  # print(len(doc_loaded))

   if not doc_loaded:
     raise FileNotFoundError(f"No PDF file has been selected in {path}")

   print("Length of PDF", len(doc_loaded))
   print("13 and 14", doc_loaded[13].page_content[:100])
   
   return doc_loaded
    
   
#document_load(path=str(data_dir))


