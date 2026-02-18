# CampusNexus AI

**Unified AI-Powered Knowledge Search for Smart Campuses**

A fully local, offline AI-powered knowledge search system that enables intelligent search across multi-modal academic content. Zero API keys required, runs completely on your machine!

## ✨ Features

- 🤖 **AI-Powered Chat**: Ask questions and get accurate answers with source citations
- 📤 **Document Upload**: Support for PDF, DOCX, and PPTX files
- 📊 **PYQ Analytics**: Analyze Previous Year Questions for patterns and insights
- 🕸️ **Knowledge Graph**: Visualize relationships between concepts
- 🌐 **Multilingual Support**: Query and respond in 5 languages (English, Hindi, Spanish, French, German)
- ⚙️ **Governance Panel**: Document approval workflow and usage statistics
- 🔒 **Fully Local**: No data leaves your machine, complete privacy
- 💯 **No API Keys**: Zero cost, no billing, completely free to run

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Ollama**: Local LLM runtime
- **Mistral**: 7B parameter language model
- **SentenceTransformers**: Local embeddings (all-MiniLM-L6-v2)
- **ChromaDB**: Vector database for semantic search
- **LangChain**: LLM orchestration

### Frontend
- **HTML5**: Semantic markup
- **Vanilla CSS**: Modern design with gradients and animations
- **JavaScript**: Interactive functionality

## 📋 Prerequisites

### 1. Install Python
- Python 3.9 or higher
- Download from: https://www.python.org/downloads/

### 2. Install Ollama

**Windows:**
1. Download Ollama from: https://ollama.ai/download/windows
2. Run the installer
3. Verify installation:
   ```bash
   ollama --version
   ```

**Mac:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 3. Pull Mistral Model

After installing Ollama, pull the Mistral model:

```bash
ollama pull mistral
```

This will download the Mistral 7B model (~4GB). First-time download may take a few minutes.

### 4. Verify Ollama is Running

Make sure Ollama service is running:

**Windows/Mac:**
- Ollama should start automatically
- Check system tray for Ollama icon

**Linux:**
```bash
ollama serve
```

Test Ollama:
```bash
ollama list
```

You should see `mistral` in the list.

## 🚀 Installation

### 1. Clone/Navigate to Project

```bash
cd c:\Users\hp\Final
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required Python packages including:
- FastAPI, Uvicorn
- LangChain, LangChain-Community
- ChromaDB
- SentenceTransformers
- Document processors (pypdf, python-docx, python-pptx)
- NetworkX for knowledge graphs

## ▶️ Running the Application

### 1. Start Ollama (if not running)

Make sure Ollama is running in the background. On Windows/Mac, it should auto-start. On Linux:

```bash
ollama serve
```

### 2. Start the Backend

From the project root directory:

```bash
python -m uvicorn backend.main:app --reload
```

Or:

```bash
python backend/main.py
```

The server will start at: `http://localhost:8000`

### 3. Access the Application

Open your web browser and navigate to:

```
http://localhost:8000
```

## 📖 Usage Guide

### 1. Upload Documents

1. Click on **📤 Upload Documents** tab
2. Drag and drop PDF, DOCX, or PPTX files
3. Or click to browse and select files
4. Wait for processing to complete
5. Documents are automatically indexed in ChromaDB

### 2. Ask Questions (RAG Chat)

1. Go to **💬 AI Chat** tab
2. Type your question in the input box
3. Press Enter or click Send
4. Get AI-generated answers with:
   - Source citations
   - Confidence scores
   - Referenced document chunks

### 3. View PYQ Analytics

1. Navigate to **📊 PYQ Analytics** tab
2. Upload PYQ (Previous Year Questions) documents
3. View:
   - Total questions analyzed
   - Topic distribution
   - Difficulty patterns
   - Year-wise trends
   - Important topics

### 4. Explore Knowledge Graph

1. Go to **🕸️ Knowledge Graph** tab
2. Click **🔄 Refresh Graph**
3. See entity relationships extracted from your documents
4. View graph statistics (nodes, edges, density)

### 5. Multilingual Support

1. Select language from dropdown in header
2. Available languages: English, Hindi, Spanish, French, German
3. Ask questions in any language
4. Responses will be in the selected language

### 6. Governance Panel

1. Access **⚙️ Governance** tab
2. View statistics:
   - Total documents
   - Pending approvals
   - Approved/rejected documents
   - Query count
3. Approve or reject uploaded documents
4. Monitor system usage

## 🔧 Configuration

Edit `backend/config.py` to customize:

- **Chunk size**: Adjust `CHUNK_SIZE` for text splitting
- **Top-K retrieval**: Modify `TOP_K_RETRIEVAL` for number of sources
- **Models**: Change `OLLAMA_MODEL` or `EMBEDDING_MODEL`
- **Languages**: Add more to `SUPPORTED_LANGUAGES`

## 🐛 Troubleshooting

### Ollama Connection Error

**Error:** "Ollama is not running"

**Solution:**
1. Make sure Ollama is installed
2. Check if Ollama service is running
3. Verify Mistral model is available: `ollama list`
4. Try running: `ollama pull mistral`

### ChromaDB Error

**Error:** "ChromaDB initialization failed"

**Solution:**
- Check write permissions in `data/chroma_db/` directory
- Delete `data/chroma_db/` folder and restart to rebuild database

### Model Not Found

**Error:** "Model 'mistral' not found"

**Solution:**
```bash
ollama pull mistral
```

### Slow Responses

**Issue:** AI responses take too long

**Solutions:**
- Use a smaller model: `ollama pull mistral:7b-instruct-v0.2-q4_0`
- Reduce `TOP_K_RETRIEVAL` in config
- Use GPU acceleration if available (set `EMBEDDING_DEVICE = "cuda"`)

### Port Already in Use

**Error:** "Port 8000 already in use"

**Solution:**
```bash
# Change port in backend/config.py or run with custom port
uvicorn backend.main:app --port 8080
```

## 📁 Project Structure

```
c:/Users/hp/Final/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration settings
│   ├── models.py               # Pydantic models
│   ├── llm/
│   │   ├── ollama_client.py    # Ollama integration
│   │   └── embeddings.py       # Local embeddings
│   ├── vector_store/
│   │   └── chroma_client.py    # ChromaDB client
│   ├── rag/
│   │   ├── retriever.py        # Document retrieval
│   │   └── generator.py        # Answer generation
│   ├── processors/
│   │   ├── pdf_processor.py    # PDF processing
│   │   ├── docx_processor.py   # DOCX processing
│   │   ├── pptx_processor.py   # PPTX processing
│   │   └── text_chunker.py     # Text chunking
│   └── features/
│       ├── pyq_analytics.py    # PYQ analysis
│       ├── knowledge_graph.py  # Graph generation
│       ├── multilingual.py     # Language support
│       └── governance.py       # Document governance
├── frontend/
│   ├── index.html              # Main HTML
│   ├── styles.css              # Styling
│   └── app.js                  # JavaScript logic
├── data/
│   └── chroma_db/              # Vector database storage
├── uploads/                    # Uploaded documents
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🎯 System Requirements

### Minimum
- **CPU**: 4 cores
- **RAM**: 8 GB
- **Storage**: 10 GB free space
- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 20.04+

### Recommended
- **CPU**: 8+ cores
- **RAM**: 16 GB+
- **Storage**: 20 GB+ SSD
- **GPU**: NVIDIA GPU with CUDA for acceleration (optional)

## 🔐 Privacy & Security

- ✅ All processing happens locally
- ✅ No data sent to external APIs
- ✅ No telemetry or tracking
- ✅ Documents stored locally
- ✅ Complete offline operation

## 📝 License

This project is created for educational purposes.

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify Ollama is running correctly
3. Ensure all dependencies are installed

## 🌟 Acknowledgments

- **Ollama**: Local LLM runtime
- **Mistral AI**: Mistral language model
- **ChromaDB**: Vector database
- **SentenceTransformers**: Embedding models
- **FastAPI**: Web framework

---

**Made with ❤️ for Smart Campuses | Fully Local | Zero API Keys | Complete Privacy**
