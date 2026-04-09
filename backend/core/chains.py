import langchain
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

from backend.prompts.templates import get_system_prompt
from backend.core.loader import load_document
from backend.core.processor import text_splitter
from backend.core.vector_store import store_vectors
from backend.core.retriever import get_retriever

load_dotenv()

# ------------- Initializing Chat & Embedding Models --------------

chat_model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash-lite",
    api_key = os.getenv("GOOGLE_API_KEY"),
    temperature = 0.2
)

embedding_model = GoogleGenerativeAIEmbeddings(
    model = "gemini-embedding-001",
    api_key = os.getenv("GOOGLE_API_KEY")
)

# ------------ Function that take query and file and return answer -------------
def answer_query(query, filepath=None):
    if not filepath:
        return "Error: Please provide a file."
        
    # Use absolute paths for production
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vector_store_path = os.path.join(base_dir, "data", "vector_store", f"vector_store_{filename}")
    
    db_exists = os.path.exists(vector_store_path) and len(os.listdir(vector_store_path)) > 0
    
    if not db_exists:
        if not filepath:
            return "Error: Database is empty. Please provide a file first."
        print(f"Vector store not found for {filename}. Creating it now...")
        document = load_document(filepath)
        chunks = text_splitter(document)
        # Chroma expects the embedding_model ITSELF, not a generated list of numbers!
        # It will use this model to internally generate the numbers inside from_documents.
        store_vectors(chunks, embedding_model, persist_directory=vector_store_path)
    else:
        print(f"Existing vector store found for {filename}. Bypassing file processing...")

    # 1. Get our retriever
    retriever = get_retriever(persist_directory=vector_store_path)
    
    # 2. Retrieve exactly what we need from vector_store
    retrieved_chunks = retriever.invoke(query)
    
    # 3. Combine chunk texts into 1 large block of context
    context_text = "\n\n".join([chunk.page_content for chunk in retrieved_chunks])
    
    # 4. Pass our question and loaded context to the Prompt Template
    prompt = get_system_prompt(pdf_chunks=context_text, user_query=query)
    
    # 5. Generate the final Answer from Gemini
    response = chat_model.invoke(prompt)
    
    return response.content

# ==== Testing ====
#print(answer_query("He is doing what", "data/vinay.txt"))
