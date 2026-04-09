from langchain_community.vectorstores import Chroma


def get_retriever(persist_directory="./data/vector_store/", embedding_model=None):
    # Pass embedding_model as an argument instead of importing from chains.py
    # to avoid circular imports.
    if embedding_model is None:
        raise ValueError("embedding_model must be provided to get_retriever")
        
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