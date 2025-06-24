import streamlit as st
from groq import Groq
from document_processor import DocumentProcessor
from vector_store import VectorStoreManager
from config import Config
import os

# Page configuration
st.set_page_config(
    page_title="DocExpy - Document Q&A System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #333;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    if 'document_processor' not in st.session_state:
        st.session_state.document_processor = DocumentProcessor()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'documents_uploaded' not in st.session_state:
        st.session_state.documents_uploaded = []

def check_api_key():
    """Check if Groq API key is configured"""
    try:
        Config.validate_config()
        return True
    except ValueError as e:
        st.error(str(e))
        st.info("Please set your GROQ_API_KEY environment variable or create a .env file.")
        return False

def setup_sidebar():
    """Setup the sidebar with configuration and status"""
    with st.sidebar:
        st.markdown("### 🔧 Configuration")
        
        # API Key status
        if Config.GROQ_API_KEY:
            st.success("✅ Groq API Key configured")
        else:
            st.error("❌ Groq API Key not found")
            st.info("Add GROQ_API_KEY to your .env file")
        
        # Model info
        st.info(f"🤖 LLM Model: {Config.LLM_MODEL}")
        st.info(f"🔗 Embedding Model: {Config.EMBEDDING_MODEL}")
        
        st.markdown("---")
        
        # Vector Store Info
        st.markdown("### 📊 Document Store Status")
        if st.session_state.vector_store:
            info = st.session_state.vector_store.get_collection_info()
            st.metric("Documents in Store", info["document_count"])
            
            if st.button("🗑️ Clear Document Store"):
                if st.session_state.vector_store.clear_collection():
                    st.session_state.documents_uploaded = []
                    st.rerun()
        else:
            st.info("No documents uploaded yet")
        
        st.markdown("---")
        
        # Uploaded Documents
        st.markdown("### 📄 Uploaded Documents")
        if st.session_state.documents_uploaded:
            for doc in st.session_state.documents_uploaded:
                st.text(f"• {doc}")
        else:
            st.text("No documents uploaded")

def upload_documents():
    """Handle document upload and processing"""
    st.markdown('<div class="sub-header">📁 Document Upload</div>', unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Choose PDF or Word documents",
        type=['pdf', 'docx', 'doc'],
        accept_multiple_files=True,
        help="Upload one or more documents to create your knowledge base"
    )
    
    if uploaded_files:
        if st.button("🚀 Process Documents", type="primary"):
            # Initialize vector store if needed
            if st.session_state.vector_store is None:
                with st.spinner("Initializing embedding model..."):
                    st.session_state.vector_store = VectorStoreManager()
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing {uploaded_file.name}...")
                
                # Process document
                chunks = st.session_state.document_processor.process_document(uploaded_file)
                
                if chunks:
                    # Add to vector store
                    success = st.session_state.vector_store.add_documents(chunks, uploaded_file.name)
                    if success and uploaded_file.name not in st.session_state.documents_uploaded:
                        st.session_state.documents_uploaded.append(uploaded_file.name)
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.text("✅ Processing complete!")
            st.rerun()

def generate_answer(query: str, context_chunks: list) -> str:
    """Generate answer using Groq API"""
    try:
        # Initialize the Groq client
        client = Groq(api_key=Config.GROQ_API_KEY)
        
        # Prepare context
        context = "\n\n".join([chunk['content'] for chunk in context_chunks])
        
        # Create prompt
        prompt = f"""Based on the following context from uploaded documents, please answer the question. 
If the answer cannot be found in the context, please say so clearly.

Context:
{context}

Question: {query}

Answer:"""
        
        # Generate response using Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=Config.LLM_MODEL,
            temperature=0.1,
            max_tokens=1024,
        )
        
        return chat_completion.choices[0].message.content or "No answer available"
        
    except Exception as e:
        return f"Error generating answer: {str(e)}"

def question_answering():
    """Handle question answering interface"""
    st.markdown('<div class="sub-header">💬 Ask Questions</div>', unsafe_allow_html=True)
    
    if not st.session_state.vector_store or not st.session_state.documents_uploaded:
        st.info("Please upload and process documents first to ask questions.")
        return
    
    # Query input
    query = st.text_input(
        "Ask a question about your documents:",
        placeholder="What is the main topic discussed in the document?",
        help="Type your question here and press Enter"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        search_button = st.button("🔍 Search", type="primary")
    with col2:
        num_results = st.selectbox("Number of context chunks:", [3, 5, 7], index=0)
    
    if query and search_button:
        with st.spinner("Searching for relevant information..."):
            # Perform similarity search
            relevant_chunks = st.session_state.vector_store.similarity_search(query, k=num_results)
            
            if relevant_chunks:
                # Generate answer
                with st.spinner("Generating answer with Groq..."):
                    answer = generate_answer(query, relevant_chunks)
                
                # Display results
                st.markdown("### 📝 Answer")
                st.markdown(f'<div class="success-box">{answer}</div>', unsafe_allow_html=True)
                
                # Show sources
                with st.expander("📚 View Source Context"):
                    for i, chunk in enumerate(relevant_chunks):
                        st.markdown(f"**Source {i+1}** (from {chunk['metadata']['filename']}):")
                        st.text(chunk['content'][:500] + "..." if len(chunk['content']) > 500 else chunk['content'])
                        st.markdown(f"*Relevance Score: {1 - chunk['distance']:.3f}*")
                        st.markdown("---")
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "question": query,
                    "answer": answer,
                    "sources": len(relevant_chunks)
                })
            else:
                st.warning("No relevant information found in the uploaded documents.")

def show_chat_history():
    """Display chat history"""
    if st.session_state.chat_history:
        st.markdown('<div class="sub-header">📜 Chat History</div>', unsafe_allow_html=True)
        
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5
            with st.expander(f"Q: {chat['question'][:50]}..."):
                st.markdown(f"**Question:** {chat['question']}")
                st.markdown(f"**Answer:** {chat['answer']}")
                st.caption(f"Sources used: {chat['sources']}")

def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">📚 DocExpy</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Document-based Question Answering System</div>', unsafe_allow_html=True)
    
    # Check API key
    if not check_api_key():
        return
    
    # Setup sidebar
    setup_sidebar()
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📁 Upload Documents", "💬 Ask Questions", "📜 History"])
    
    with tab1:
        upload_documents()
    
    with tab2:
        question_answering()
    
    with tab3:
        show_chat_history()
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #666;">Built with Streamlit, LangChain, and Groq API</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 