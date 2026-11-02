from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

def get_embedding():
    #doc_chunks = split_document()
    embed = OpenAIEmbeddings(model="text-embedding-3-large")
   # embed_doc = embed.embed_documents([doc.page_content  for doc in doc_chunks])
    #print("Embed doc==>",len(embed_doc))
    #print("EMbedding",len(embed))
    #print("Check embed",len(embed_doc[0]))# Each chunck/vector containing 3072 number representation
    #In ops_documentatioSn case we have chunk size of 1000 and total number of chunks/vector is 824
    #Each chunk contain 3072 numbers
    return embed

#get_embedding()


