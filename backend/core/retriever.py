from langchain_community.vectorstores import Chroma


def get_retriever(persist_directory="./data/vector_store/"):
    # We load the vector database that was saved to disk earlier, 
    # rather than creating a new one with store_vectors()
    from backend.core.chains import embedding_model
    vector_store = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    return retriever

# ================== This is for testing purpose ==================
"""
retriever = get_retriever()
retrieved_chunks = retriever.invoke("What is the capital of France?")
print(f"Retrieved {len(retrieved_chunks)} chunks")
if len(retrieved_chunks) > 0:
    print(retrieved_chunks[0].page_content)
else:
    print("No chunks retrieved.")
"""