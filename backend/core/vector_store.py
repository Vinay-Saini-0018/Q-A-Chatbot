from langchain_community.vectorstores import Chroma

def store_vectors(chunks,embedding_model, persist_directory="./data/vector_store/"):
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )

    return vector_store

