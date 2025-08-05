from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter,
    MarkdownHeaderTextSplitter,
    HTMLHeaderTextSplitter,
    SentenceTransformersTokenTextSplitter
)
from typing import List, Optional, Dict, Any


class TextChunker:
    """
    A utility class for chunking text using various LangChain text splitters.
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the text chunker with default parameters.
        
        Args:
            chunk_size: Maximum size of each chunk
            chunk_overlap: Overlap between consecutive chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize the default recursive splitter
        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def chunk_text_recursive(self, text: str) -> List[str]:
        """
        Split text using RecursiveCharacterTextSplitter (recommended for most use cases).
        
        Args:
            text: The text to split
            
        Returns:
            List of text chunks
        """
        return self.recursive_splitter.split_text(text)
    
    def chunk_text_character(self, text: str, separator: str = "\n") -> List[str]:
        """
        Split text using CharacterTextSplitter.
        
        Args:
            text: The text to split
            separator: Character to split on
            
        Returns:
            List of text chunks
        """
        splitter = CharacterTextSplitter(
            separator=separator,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len
        )
        return splitter.split_text(text)
    
    def chunk_text_token(self, text: str, model_name: str = "gpt-3.5-turbo") -> List[str]:
        """
        Split text using TokenTextSplitter (useful for token-aware splitting).
        
        Args:
            text: The text to split
            model_name: The model name for token counting
            
        Returns:
            List of text chunks
        """
        splitter = TokenTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            model_name=model_name
        )
        return splitter.split_text(text)
    

    
    def chunk_text_sentence_transformers(self, text: str, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> List[str]:
        """
        Split text using SentenceTransformersTokenTextSplitter.
        
        Args:
            text: The text to split
            model_name: The sentence transformer model name
            
        Returns:
            List of text chunks
        """
        splitter = SentenceTransformersTokenTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            model_name=model_name
        )
        return splitter.split_text(text)
    
    def chunk_text_arabic_optimized(self, text: str) -> List[str]:
        """
        Split Arabic text with optimizations for Arabic language characteristics.
        
        Args:
            text: The Arabic text to split
            
        Returns:
            List of text chunks
        """
        # Custom separators optimized for Arabic text
        arabic_separators = [
            "\n\n",  # Paragraph breaks
            "\n",    # Line breaks
            ". ",    # Sentence endings
            "؟ ",    # Question mark
            "! ",    # Exclamation mark
            "، ",    # Arabic comma
            "؛ ",    # Arabic semicolon
            " ",     # Space
            ""       # Character level
        ]
        
        arabic_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=arabic_separators
        )
        
        return arabic_splitter.split_text(text)
    