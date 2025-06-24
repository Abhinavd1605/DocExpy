import streamlit as st
import PyPDF2
import docx
from io import BytesIO
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import Config

class DocumentProcessor:
    """Handles document processing including text extraction and chunking"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_file = BytesIO(file_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            st.error(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    def extract_text_from_docx(self, file_bytes: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            docx_file = BytesIO(file_bytes)
            doc = docx.Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            st.error(f"Error extracting text from DOCX: {str(e)}")
            return ""
    
    def extract_text(self, uploaded_file) -> Optional[str]:
        """Extract text from uploaded file based on file type"""
        if uploaded_file is None:
            return None
        
        file_extension = uploaded_file.name.lower().split('.')[-1]
        file_bytes = uploaded_file.read()
        
        if file_extension == 'pdf':
            return self.extract_text_from_pdf(file_bytes)
        elif file_extension in ['docx', 'doc']:
            return self.extract_text_from_docx(file_bytes)
        else:
            st.error(f"Unsupported file type: {file_extension}")
            return None
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks for vector embedding"""
        if not text:
            return []
        
        chunks = self.text_splitter.split_text(text)
        return chunks
    
    def process_document(self, uploaded_file) -> List[str]:
        """Complete document processing pipeline"""
        # Extract text
        text = self.extract_text(uploaded_file)
        if not text:
            return []
        
        # Chunk text
        chunks = self.chunk_text(text)
        
        # Add metadata about the source file
        processed_chunks = []
        for i, chunk in enumerate(chunks):
            processed_chunks.append(chunk)
        
        return processed_chunks 