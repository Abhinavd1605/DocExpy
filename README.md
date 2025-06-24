# DocExpy - Document-based Question Answering System

A powerful Generative AI application that allows users to upload documents (PDFs, Word files) and ask intelligent questions based on the content using LLMs and vector search. Now powered by **Groq** for ultra-fast inference!

## 🚀 Features

- **📁 File Upload**: Support for PDF and Word documents (.pdf, .docx, .doc)
- **🔧 Intelligent Processing**: Automatic text extraction and chunking
- **🧠 Vector Embeddings**: Uses Sentence Transformers for semantic understanding
- **💬 Context-Aware Q&A**: Groq-powered question answering with document context
- **📊 Vector Search**: ChromaDB for efficient similarity search
- **🎨 Professional UI**: Clean, modern Streamlit interface
- **📜 Chat History**: Track previous questions and answers
- **🔍 Source Attribution**: Shows relevant document chunks used for answers
- **⚡ Ultra-Fast**: Groq's lightning-fast inference speeds

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM Framework**: LangChain
- **Language Model**: Groq API (Llama 3, Mixtral, Gemma models)
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Database**: ChromaDB
- **Document Processing**: PyPDF2, python-docx

## 📋 Prerequisites

- Python 3.8 or higher
- Groq API key (free at console.groq.com)

## 🔧 Installation

1. **Clone or download the project**:
   ```bash
   cd DocExpy
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `env_example.txt` content to create `.env` file
   - Add your Groq API key:
   ```bash
   # Create .env file with:
   GROQ_API_KEY=your_groq_api_key_here
   ```

## 🚀 Running the Application

1. **Start the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and navigate to `http://localhost:8501`

## 📖 How to Use

### 1. Upload Documents
- Go to the "📁 Upload Documents" tab
- Select one or more PDF or Word documents
- Click "🚀 Process Documents" to extract and embed the content

### 2. Ask Questions
- Switch to the "💬 Ask Questions" tab
- Type your question about the uploaded documents
- Click "🔍 Search" to get AI-powered answers
- View source context to see which document sections were used

### 3. Review History
- Check the "📜 History" tab to see previous questions and answers

## ⚙️ Configuration

The application can be configured through the `config.py` file:

- **CHUNK_SIZE**: Size of text chunks for processing (default: 1000)
- **CHUNK_OVERLAP**: Overlap between chunks (default: 200)
- **EMBEDDING_MODEL**: Sentence transformer model (default: all-MiniLM-L6-v2)
- **LLM_MODEL**: Groq model for Q&A (default: llama3-8b-8192)

## 🤖 Available Groq Models

- **llama3-8b-8192**: Fastest, good quality (default)
- **llama3-70b-4096**: Higher quality, slower
- **mixtral-8x7b-32768**: Balanced performance
- **gemma-7b-it**: Google's Gemma model

## 📁 Project Structure

```
DocExpy/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration management
├── document_processor.py  # Document processing utilities
├── vector_store.py       # Vector database management
├── requirements.txt      # Python dependencies
├── env_example.txt       # Environment variables template
├── README.md            # This file
└── chroma_db/           # ChromaDB storage (created automatically)
```

## 🔒 Security Notes

- Never commit your `.env` file with real API keys
- Keep your Groq API key secure
- The vector database is stored locally in the `chroma_db/` directory

## 🐛 Troubleshooting

### Common Issues:

1. **"GROQ_API_KEY environment variable is required"**
   - Make sure you've created a `.env` file with your API key

2. **File upload errors**
   - Ensure your PDF/Word files are not corrupted
   - Check file size limits (10MB max by default)

3. **Memory issues with large documents**
   - Try reducing CHUNK_SIZE in config.py
   - Process fewer documents at once

4. **Slow embedding generation**
   - First time will be slower as the model downloads
   - Subsequent runs will be much faster

## 🌟 Why Groq?

- **Ultra-fast inference**: 300+ tokens/second
- **Cost-effective**: Free tier with generous limits
- **Multiple models**: Support for Llama 3, Mixtral, and Gemma
- **High quality**: State-of-the-art model performance
- **Easy integration**: Simple API similar to OpenAI

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Groq for ultra-fast LLM inference
- Sentence Transformers for embeddings
- LangChain for the AI framework
- ChromaDB for vector storage
- Streamlit for the web interface