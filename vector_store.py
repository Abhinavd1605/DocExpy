import streamlit as st
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, cast
import hashlib
import os
from config import Config

class VectorStoreManager:
    """Manages vector database operations using ChromaDB"""
    
    def __init__(self):
        # Initialize sentence transformer for embeddings
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        
        # Initialize ChromaDB
        os.makedirs(Config.VECTOR_DB_PATH, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=Config.VECTOR_DB_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=Config.COLLECTION_NAME)
        except:
            self.collection = self.client.create_collection(
                name=Config.COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
    
    def _generate_document_id(self, filename: str, chunk_index: int) -> str:
        """Generate unique ID for document chunk"""
        content = f"{filename}_{chunk_index}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def add_documents(self, chunks: List[str], filename: str) -> bool:
        """Add document chunks to vector store"""
        try:
            if not chunks:
                st.warning("No chunks to add to vector store")
                return False
            
            # Generate embeddings using sentence transformers
            with st.spinner("Generating embeddings..."):
                embeddings = self.embedding_model.encode(chunks, convert_to_tensor=False)
                # Convert to list of lists for ChromaDB
                embeddings = embeddings.tolist()
            
            # Prepare data for ChromaDB
            ids = [self._generate_document_id(filename, i) for i in range(len(chunks))]
            metadatas = []
            for i, chunk in enumerate(chunks):
                metadata = {
                    "filename": str(filename),
                    "chunk_index": int(i),
                    "chunk_length": int(len(chunk))
                }
                metadatas.append(metadata)
            
            # Add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            
            st.success(f"Successfully added {len(chunks)} chunks to vector store")
            return True
            
        except Exception as e:
            st.error(f"Error adding documents to vector store: {str(e)}")
            return False
    
    def similarity_search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Perform similarity search for relevant document chunks"""
        try:
            # Generate query embedding using sentence transformers
            query_embedding = self.embedding_model.encode([query], convert_to_tensor=False)
            query_embedding = query_embedding.tolist()[0]
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            formatted_results = []
            if results and results.get('documents') and results['documents'] and results['documents'][0]:
                documents = results['documents'][0]
                
                # Safely get metadatas
                metadatas_list = results.get('metadatas', [[]])
                metadatas = metadatas_list[0] if metadatas_list and len(metadatas_list) > 0 else []
                
                # Safely get distances
                distances_list = results.get('distances', [[]])
                distances = distances_list[0] if distances_list and len(distances_list) > 0 else []
                
                for i in range(len(documents)):
                    formatted_results.append({
                        'content': documents[i],
                        'metadata': metadatas[i] if i < len(metadatas) else {},
                        'distance': distances[i] if i < len(distances) else 0.0
                    })
            
            return formatted_results
            
        except Exception as e:
            st.error(f"Error during similarity search: {str(e)}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the current collection"""
        try:
            count = self.collection.count()
            return {
                "document_count": count,
                "collection_name": Config.COLLECTION_NAME
            }
        except Exception as e:
            st.error(f"Error getting collection info: {str(e)}")
            return {"document_count": 0, "collection_name": Config.COLLECTION_NAME}
    
    def clear_collection(self) -> bool:
        """Clear all documents from the collection"""
        try:
            # Delete the existing collection
            self.client.delete_collection(name=Config.COLLECTION_NAME)
            
            # Create a new empty collection
            self.collection = self.client.create_collection(
                name=Config.COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            
            st.success("Vector store cleared successfully")
            return True
            
        except Exception as e:
            st.error(f"Error clearing vector store: {str(e)}")
            return False 