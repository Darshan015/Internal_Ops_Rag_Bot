from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from src.ops_vector_store.data_vector import cached_qdrant
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import time
from langchain_core.caches import InMemoryCache
import langchain_core.globals as langchain_globals
import streamlit as st

if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False

if "agent" not in st.session_state:
    st.session_state.agent = None

if "messages" not in st.session_state:
    st.session_state.messages = []

vector_store = cached_qdrant()
memory = InMemorySaver()

@tool
def get_retrieve_context(query:str):
    """This function retrieves relevant context from the vector store based on the provided query. It performs a similarity search to find the top K most similar documents to the query and returns their content as a concatenated string.
    """
    #query = "What is the fullform of GOP?"
    start = time.perf_counter()
    retrive_context = vector_store.similarity_search_with_score(query=query, k = 5)
        # result = vector_store.similarity_search_with_score(query=query, k = 3)
         #for doc, score in result:
          #print(f"* [SIM={score:3f}] {doc.page_content} [{doc.metadata}]")
    total_retrivel_time = (time.perf_counter()-start)*1000

    print(f"Total retrivel time {total_retrivel_time}")
    context = []

    for res, score in retrive_context:

        context.append(f"""
        Score: {score}
        Source: {res.metadata.get('source', 'N/A')}
        Content: {res.page_content}
        """)

    
    return "\n\n".join(context)

langchain_globals.set_llm_cache(InMemoryCache())
llm = ChatGroq(model = "openai/gpt-oss-20b")
system_prompt = """
You are a helpful assistant specializing in the SingleView operational application.

You have access to a tool called get_retrieve_context that retrieves
relevant information from the SingleView documentation.

Instructions:
1. Use the retrieval tool for SingleView-related questions.
2. Use the actual user question as the retrieval query.
3. Answer using the retrieved documentation.
4. Do not invent technical information.
5. If the answer is unavailable in the retrieved context, clearly state that.
When answering questions:

1. Use the retrieved context to formulate your answer.
2. Include the source PDF filename and page number for factual claims.
3. Never invent page numbers or sources.
4. If the retrieved context does not contain the answer, explicitly say so."""
#query = input("Enter your query: ")

agent = create_agent(
    model=llm,
    tools = [get_retrieve_context],
    system_prompt = system_prompt,
    checkpointer=memory
)
st.session_state.document_uploaded = True
st.session_state.agent = agent


def generate_response(query:str, thread_id:str):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    start = time.perf_counter()
    res = agent.invoke({"messages":[{"role":"user","content":query}]}, config = config)

    total_agentic_time = (time.perf_counter()-start)*1000
    print(res["messages"][-1].content)
    print(f"Total Agentic time taken{total_agentic_time}")
    return res["messages"][-1].content
        
  




