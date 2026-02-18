# CampusNexus AI - Quick Setup Guide

## 🚀 Step-by-Step Setup Instructions

### Step 1: Install Ollama

**Ollama is required** to run the local Mistral AI model.

#### Windows:
1. Download Ollama from: **https://ollama.ai/download/windows**
2. Run the installer (`OllamaSetup.exe`)
3. Follow the installation wizard
4. Ollama will start automatically after installation

#### Verify Ollama Installation:
Open PowerShell and run:
```powershell
ollama --version
```

You should see the Ollama version number.

---

### Step 2: Pull the Mistral Model

After Ollama is installed, download the Mistral model:

```powershell
ollama pull mistral
```

This will download ~4GB of data. Wait for it to complete.

**Verify the model is downloaded:**
```powershell
ollama list
```

You should see `mistral` in the list.

---

### Step 3: Install Python Dependencies

Navigate to the project directory and install requirements:

```powershell
cd c:\Users\hp\Final
pip install -r requirements.txt
```

If you encounter permission errors, use:
```powershell
pip install --user -r requirements.txt
```

---

### Step 4: Start the Backend Server

Run the FastAPI backend:

```powershell
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the quick start script:
```powershell
.\start.bat
```

You should see output like:
```
✓ Ollama client initialized with model: mistral
✓ ChromaDB initialized at c:\Users\hp\Final\data\chroma_db
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

### Step 5: Access the Application

Open your web browser and navigate to:

```
http://localhost:8000
```
You should see the CampusNexus AI interface!

---

## 🎯 How to Use the Application

### 1. Upload Documents
- Click on **📤 Upload Documents** tab
- Drag & drop PDF, DOCX, or PPTX files
- Or click to browse and select files
- Wait for processing to complete

### 2. Ask Questions (RAG Chat)
- Go to **💬 AI Chat** tab
- Type your question
- Press Enter or click Send
- Get AI-generated answers with sources and confidence scores

### 3. View PYQ Analytics
- Navigate to **📊 PYQ Analytics** tab
- See analysis of uploaded Previous Year Questions
- View topic distribution, difficulty patterns, and trends

### 4. Explore Knowledge Graph
- Go to **🕸️ Knowledge Graph** tab
- Click **🔄 Refresh Graph**
- View entity relationships extracted from documents

### 5. Governance Panel
- Access **⚙️ Governance** tab
- View system statistics
- Approve/reject uploaded documents
- Monitor usage

---

## 🔧 Troubleshooting

### Error: "Ollama is not running"

**Solution:**
1. Make sure Ollama is installed
2. Check if Ollama is running (should auto-start on Windows)
3. Try running: `ollama serve` in a new terminal
4. Verify model is available: `ollama list`

### Error: "Model 'mistral' not found"

**Solution:**
```powershell
ollama pull mistral
```

### Port Already in Use

**Solution:**
Run on a different port:
```powershell
python -m uvicorn backend.main:app --reload --port 8080
```

Then access at: http://localhost:8080

### Slow Responses

**Solutions:**
- Use a smaller/quantized model: `ollama pull mistral:7b-instruct-v0.2-q4_0`
- Close other applications to free up RAM
- Reduce `TOP_K_RETRIEVAL` in `backend/config.py`

---

## 📝 System Requirements

### Minimum:
- **CPU**: 4 cores
- **RAM**: 8 GB
- **Storage**: 10 GB free
- **OS**: Windows 10/11

### Recommended:
- **CPU**: 8+ cores
- **RAM**: 16 GB+
- **Storage**: 20 GB+ SSD
- **GPU**: NVIDIA GPU with CUDA (optional, for faster processing)

---

## ✅ Checklist

Before running the application, make sure:

- [ ] Ollama is installed (`ollama --version` works)
- [ ] Mistral model is downloaded (`ollama list` shows mistral)
- [ ] Python dependencies are installed
- [ ] Ollama service is running
- [ ] Port 8000 is available

---

## 🎉 Ready to Go!

Once all steps are complete:
1. Start the backend: `python -m uvicorn backend.main:app --reload`
2. Open browser: http://localhost:8000
3. Upload documents and start chatting!

**Need help?** Check the main README.md for detailed documentation.
