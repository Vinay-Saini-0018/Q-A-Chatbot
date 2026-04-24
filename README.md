# 📄 Q&A Chatbot — PDF Document Intelligence

A full-stack RAG (Retrieval-Augmented Generation) chatbot that lets you upload PDF documents and ask questions about their content in natural language. Powered by **Google Gemini**, **LangChain**, **LangGraph**, and **ChromaDB**, with a clean frontend and a production-ready FastAPI backend.

---

## 📄 Q&A Chatbot — PDF Document Intelligence

🔗 **[Live Demo](https://q-a-chatbot-3.onrender.com/)**

## ✨ Features

- 📁 **PDF Upload** — Upload one or more PDF documents through the UI
- 🔍 **Semantic Search** — ChromaDB vector store retrieves the most relevant document chunks
- 🤖 **AI-Powered Q&A** — Google Gemini generates accurate, context-aware answers
- ⚡ **FastAPI Backend** — Clean REST API with async support

---

## 🗂️ Project Structure

```
Q-A-Chatbot/
├── backend/               # FastAPI application
│   ├── main.py            # API entry point & routes
│   ├── services/          # RAG pipeline, embeddings, LangGraph agent
│   └── config/            # Environment & app configuration
├── frontend/              # HTML/CSS/JS chat interface
├── data/                  # Uploaded PDF storage
├── docker-compose.yml     # Docker orchestration (app + PostgreSQL)
├── requirements.txt       # Python dependencies
└── .gitignore
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Google Gemini (`langchain-google-genai`) |
| Orchestration | LangChain + LangGraph |
| Vector Store | ChromaDB |
| Memory / Checkpointing |
| Backend | FastAPI + Uvicorn |
| PDF Parsing | PyPDF + Unstructured |
| Frontend | HTML, CSS, JavaScript |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A [Google AI Studio](https://aistudio.google.com/) API key (free tier available)

### 1. Clone the Repository

```bash
git clone https://github.com/Vinay-Saini-0018/Q-A-Chatbot.git
cd Q-A-Chatbot
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```


### 3. Run Locally (Without Docker)

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend
uvicorn backend.main:app --reload --port 8000

# Start the frontend
python -m http.server 3000
```

Then open `localhost:3000/frontend/index.html` in your browser.

---

## 💬 How to Use

1. Open the app in your browser (`http://localhost:8000` or the frontend HTML).
2. Upload a PDF file using the upload button.
3. Wait for the document to be processed and indexed.
4. Type your question in the chat box and hit **Send**.
5. The chatbot will respond with an answer grounded in your document's content.

---

## 🧩 How It Works

```
User uploads PDF
        ↓
PDF is parsed & split into chunks (PyPDF / Unstructured)
        ↓
Chunks are embedded & stored in ChromaDB
        ↓
User asks a question
        ↓
LangGraph agent retrieves relevant chunks from ChromaDB
        ↓
Google Gemini generates an answer using retrieved context
        ↓
Answer returned to user 
```

---

## 📦 Dependencies

Key packages from `requirements.txt`:

- `langchain`, `langchain-core`, `langchain-community`
- `langchain-google-genai`, `google-generativeai`
- `langgraph`, `langgraph-checkpoint-postgres`
- `chromadb`
- `fastapi`, `uvicorn`, `pydantic`, `python-multipart`
- `pypdf`, `unstructured`, `python-docx`
- `psycopg[binary,pool]`
- `python-dotenv`

---

## 🔮 Roadmap

- [ ] Support for `.docx` and `.txt` file uploads
- [ ] Multiple document sessions
- [ ] Streaming responses
- [ ] Deployed live demo

---

## 👤 Author

**Vinay Saini**  
AI/ML Developer · [GitHub](https://github.com/Vinay-Saini-0018)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
