from langchain_community.document_loaders import PyPDFLoader,TextLoader,UnstructuredWordDocumentLoader

# ---------- Function that will load all type of file ---------
def load_document(file):
    if file.endswith(".txt"):
        loader = TextLoader(file)
    elif file.endswith(".pdf"):
        loader = PyPDFLoader(file)
    elif file.endswith(".docx"):
        loader = UnstructuredWordDocumentLoader(file)
    else:
        raise ValueError("Unsupported file type")

    document = loader.load()
    return document
