import time

from dotenv import load_dotenv
load_dotenv()
from qdrant_client.http import models
from src.ops_embedder.data_embedding import get_embedding
from src.ops_chunking.data_chunking import split_document
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore,RetrievalMode,FastEmbedSparse
from qdrant_client import QdrantClient
from pathlib import Path
from uuid import uuid4
from qdrant_client.http.models import Distance, SparseVectorParams, VectorParams

qdrant_db_path = Path(__file__).resolve().parents[3] / "tmp" / "qdrant_db"
client = QdrantClient(path=str(qdrant_db_path))


def cached_qdrant():
     
     
     if not client.collection_exists("Singleview Ops"):
         client.close()
         raise RuntimeError("Collection 'Singleview Ops' does not exist. Please create the collection first.")
     print("\n\n Entering cached_qdrant function \n\n")
     embed = get_embedding()
     sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")
     vector_store = QdrantVectorStore(
                client=client,
                collection_name="Singleview Ops",
                embedding=embed,
                sparse_embedding=sparse_embeddings,
                retrieval_mode=RetrievalMode.HYBRID,
                vector_name="dense",
                sparse_vector_name="sparse",
           )
     return vector_store 
     

def define_qdrantDb():
    
     embed = get_embedding()
     doc_chunks = split_document()
     vector_size = len(embed.embed_query("test"))
     print("\n\n Entring define_qdrantDb function \n\n")
     sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")
     print("Vector_size",vector_size)
     if client.collection_exists("Singleview Ops"):
          client.delete_collection("Singleview Ops")

     if not client.collection_exists("Singleview Ops"):
          client.create_collection(
               collection_name="Singleview Ops",
               vectors_config={"dense":VectorParams(size=vector_size, distance=Distance.COSINE)},
               sparse_vectors_config={"sparse": SparseVectorParams(index=models.SparseIndexParams(on_disk=False))},
          )

     vector_store = QdrantVectorStore(
          client=client,
          collection_name="Singleview Ops",
          embedding=embed,
          sparse_embedding=sparse_embeddings,
          retrieval_mode=RetrievalMode.HYBRID,
          vector_name="dense",
          sparse_vector_name="sparse",

     )

     uuids = [str(uuid4()) for _ in range(len(doc_chunks))]
     start = time.perf_counter()
     vector_store.add_documents(documents=doc_chunks, ids=uuids)
     Total_embedding_time = (time.perf_counter()-start)*1000
     print(f"Total embedding time {Total_embedding_time}")
    
     client.close()

#define_qdrantDb()


#Need to check #retrivel latency/Retrival relevance/Throughput(how many queries processed per second)
#/Scalability(how well the system can handle increasing amounts of data or traffic)
# Fault tolerance (how well the system can recover from failures or errors)/Cost (how much it costs to run and maintain the system)
#Similarity/distance score

#Method tried to retrive the relevant context:
#1.Updating the value of K in similarity search(to get the top K most similar documents to the query) 



