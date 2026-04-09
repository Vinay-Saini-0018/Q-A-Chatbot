from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.core.loader import load_document

# --------- Function that will chunk the documents -----------

def text_splitter(document):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=30
    )

    chunks = splitter.split_documents(document)
    return chunks


