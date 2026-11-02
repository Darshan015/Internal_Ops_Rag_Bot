from src.ops_ingestion.data_loader import document_load
from pathlib import Path

data_dir = Path(__file__).resolve().parents[2] / "data"



def test_loading():
     doc_loaded = document_load(path=str(data_dir))
     assert len(doc_loaded) > 0, "No PDF pages were loaded"
     empty_pages = [
         doc for doc in doc_loaded
         if not doc.page_content.strip()
         ]
     
     
     print("Length of empty page",len(empty_pages))
       #Empty pages should be removed as it often consume resources in vector db,
       # resulting in useless embedding and 
       #hamper the retrivel quality/context

     for doc in empty_pages:             
              print(
                   "Empty page:",
                   doc.metadata.get("page", "Unknown")
               )
              assert len(empty_pages)==0, "Empty Pages Detected" #Assertion occur only if the conditiona fails
              

  