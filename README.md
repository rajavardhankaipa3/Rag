# PDF RAG Chatbot

### AI-Powered PDF Question Answering System using Retrieval-Augmented Generation

A Python-based web application that enables users to upload PDF documents and ask natural-language questions about their content using **Retrieval-Augmented Generation (RAG)**.

The application combines semantic search using **Sentence Transformers and FAISS** with the **xAI Grok API** to generate context-aware responses based on relevant information retrieved from uploaded documents.

## Project Overview

Reading and searching through lengthy PDF documents can be time-consuming. This project provides an interactive question-answering interface that helps users retrieve relevant information without manually searching through every page.

The system extracts text from an uploaded PDF, divides it into manageable chunks, converts the chunks into vector embeddings, and indexes them using FAISS.

When a user submits a question, the application performs semantic similarity search to retrieve relevant document sections. These sections are supplied to the Grok language model to generate an answer grounded in the retrieved context.

## Key Features

- **PDF Upload:** Upload text-based PDF documents through a Streamlit interface.
- **Text Extraction:** Extract document content using PyMuPDF.
- **Text Chunking:** Divide extracted content into smaller, overlapping chunks.
- **Semantic Embeddings:** Generate vector representations using Sentence Transformers.
- **Vector Similarity Search:** Retrieve relevant document chunks using FAISS.
- **RAG-Based Question Answering:** Combine retrieved content with Grok-generated responses.
- **Source References:** Display relevant PDF page numbers and retrieved text.
- **Interactive Interface:** Ask questions through a simple Streamlit web application.
- **Local Embeddings:** Generate embeddings locally without requiring a paid embedding API.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Streamlit | Web interface |
| PyMuPDF | PDF text extraction |
| Sentence Transformers | Text embeddings |
| all-MiniLM-L6-v2 | Embedding model |
| FAISS | Vector similarity search |
| Grok API (xAI) | Language model for answer generation |
| NumPy | Numerical processing |
| python-dotenv | Environment variable management |

## System Architecture

```text
                  PDF Document
                       |
                       v
                 Text Extraction
                       |
                       v
                  Text Chunking
                       |
                       v
               Sentence Transformers
                       |
                       v
                  FAISS Index
                       |
                       |
User Question ----------+
       |
       v
Question Embedding
       |
       v
Semantic Similarity Search
       |
       v
Relevant Document Chunks
       |
       v
Grok Language Model
       |
       v
Generated Answer + Source Pages
```

## How RAG Works

**1. Document Upload**

The user uploads a PDF through the Streamlit application.

**2. Text Extraction**

PyMuPDF extracts text from the document while retaining page-number information.

**3. Text Chunking**

Extracted text is divided into smaller overlapping segments to support efficient retrieval.

**4. Embedding Generation**

Sentence Transformers converts each text chunk into a numerical vector representing its semantic meaning.

**5. Vector Indexing**

FAISS stores the embeddings in an in-memory vector index.

**6. Question Processing**

The user's question is converted into an embedding using the same embedding model.

**7. Context Retrieval**

FAISS identifies the most relevant document chunks based on vector similarity.

**8. Answer Generation**

The retrieved chunks and user question are provided to the Grok API, which generates a response using the supplied context.

## Project Structure

```text
PDF-RAG-GROK/
|
|-- app.py
|-- rag.py
|-- pdf_processor.py
|-- vector_store.py
|-- grok_api.py
|-- requirements.txt
|-- .gitignore
|-- .env.example
|-- README.md
|
|-- data/
|   |-- uploads/
|
|-- venv/                 # Ignored by Git
|-- .env                  # Ignored by Git
```

### File Descriptions

| File | Description |
|---|---|
| app.py | Streamlit application and user interface |
| rag.py | Coordinates document processing, retrieval, and answer generation |
| pdf_processor.py | Extracts PDF text and creates chunks |
| vector_store.py | Generates embeddings and performs FAISS similarity search |
| grok_api.py | Integrates the xAI Grok API |
| requirements.txt | Python dependencies |
| .env | Stores the private API key locally |
| .gitignore | Excludes sensitive and generated files |

## Installation and Setup

### Prerequisites

- Python 3.10 or later with compatible dependencies
- pip
- Git
- VS Code or another code editor
- An xAI API key with access to a supported Grok model

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/PDF-RAG-Chatbot.git
cd PDF-RAG-Chatbot
```

Replace `YOUR_USERNAME` with your GitHub username.

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure the API Key

Create a `.env` file in the project root:

```dotenv
XAI_API_KEY=your_xai_api_key_here
```

Obtain an API key from the official [xAI Console](https://console.x.ai/).

The Grok API may incur usage charges. Local embedding generation and FAISS indexing do not require a paid embedding API.

Never commit your real `.env` file or API key to GitHub.

### Step 5: Run the Application

```bash
streamlit run app.py
```

Open the application at:

http://localhost:8501

## How to Use

1. Launch the Streamlit application.
2. Upload a text-based PDF using the sidebar.
3. Click **Process PDF**.
4. Wait for text extraction, embedding generation, and FAISS indexing to complete.
5. Enter a question related to the uploaded document.
6. Click **Ask Grok**.
7. View the generated answer and relevant PDF source pages.

### Example

**Uploaded Document:** `machine_learning_notes.pdf`

**User Question:**

What is supervised learning?

**Example Answer:**

Supervised learning is a machine learning approach in which a model learns from labeled training data to make predictions on new inputs.

**Relevant Sources:** Pages 3 and 4, depending on the uploaded document.

*The example is illustrative; actual answers depend on the document content.*

## Current Limitations

- The implementation processes one PDF at a time.
- Scanned or image-only PDFs may require OCR support.
- The FAISS index is stored in application memory and is not automatically persisted between restarts.
- Answer quality depends on the extracted document text, retrieved chunks, and language model.
- Source page references identify retrieved context and do not independently guarantee answer correctness.
- Grok API access requires valid credentials and may involve usage costs.
- The current implementation does not include user authentication or persistent conversation history.

## Future Enhancements

- Support for uploading and querying multiple PDF documents
- Chat-style interface with conversation history
- OCR integration for scanned documents
- Persistent vector database storage
- Improved retrieval and reranking
- More precise source citations
- Support for additional document formats
- User authentication and document management
- Cloud deployment
- Improved error handling and retrieval evaluation

## Learning Outcomes

This project demonstrates practical experience with:

- Retrieval-Augmented Generation architecture
- Natural Language Processing
- Semantic embeddings
- Vector similarity search
- PDF document processing
- Large Language Model API integration
- Python application development
- Streamlit-based web interfaces
- Modular software design

## Security Considerations

API credentials are stored in environment variables rather than hardcoded in the application.

The `.gitignore` file excludes local secrets, virtual environments, uploaded documents, and generated vector indexes.

Uploaded PDF content may be sent to the configured external language model API as retrieved context. Avoid uploading confidential documents unless the relevant data-handling requirements are satisfied.

## Author

**Kaipa Venkata Raja Vardhan Reddy**

B.Tech – Computer Science and Engineering  
KL University

## Project Status

**Local prototype**

The project provides a foundational PDF question-answering workflow using RAG, FAISS, Sentence Transformers, Streamlit, and Grok API integration. Additional features and deployment improvements are planned.

---

*Built to explore practical applications of Generative AI, semantic search, and Retrieval-Augmented Generation.*
