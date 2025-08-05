import os
import sys
import tempfile
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import transaction

# Add the ai_workflow project to Python path
ai_workflow_path = Path(settings.BASE_DIR) / 'ai_workflow'
sys.path.append(str(ai_workflow_path))

from src.preprocessors.text_splitters import TextChunker
from src.graphs.graph_builders import compiled_graph
from src.schemas.states import State, initial_state
from src.configs import config
from chunks.models import Chunk
from profiles.models import Profile
from books.models import Book


class AIBookProcessor:
    """
    Service class to process books using the AI workflow and store results in Django models.
    """
    
    def __init__(self):
        self.chunker = TextChunker(chunk_size=5000, chunk_overlap=200)
    
    def process_book(self, book: Book) -> Dict[str, Any]:
        """
        Process a book through the AI workflow and store chunks and profiles in Django models.
        
        Args:
            book: The Book instance to process
            
        Returns:
            Dictionary with processing results
        """
        try:
            # Get the book file path
            if not book.file:
                raise ValueError("Book has no file attached")
            
            file_path = book.file.path
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Book file not found: {file_path}")
            
            # Clear any existing analysis for this book
            self.delete_book_analysis(book)
            
            # Create a temporary file for the AI workflow
            temp_file_path = self._create_temp_file_from_book(book)
            
            try:
                # Initialize state for AI workflow
                state = initial_state.copy()
                state['file_path'] = temp_file_path
                
                # Run the AI workflow
                response = compiled_graph.invoke(state, config=config)
                
                # Extract chunks and profiles from AI response and store in Django
                chunks_created, profiles_created = self._extract_from_ai_response(book, response)
                
                return {
                    'success': True,
                    'chunks_created': chunks_created,
                    'profiles_created': profiles_created,
                    'book_id': book.id
                }
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'book_id': book.id if book else None
            }
    
    def _create_temp_file_from_book(self, book: Book) -> str:
        """
        Create a temporary file from book content for the AI workflow.
        
        Args:
            book: The Book instance
            
        Returns:
            Path to the temporary file
        """
        # Read the book content
        with open(book.file.path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
        temp_file.write(text)
        temp_file.close()
        
        return temp_file.name
    
    def _extract_from_ai_response(self, book: Book, ai_response: Dict[str, Any]) -> Tuple[int, int]:
        """
        Extract chunks and profiles from AI response and store in Django models.
        
        Args:
            book: The Book instance
            ai_response: Response from the AI workflow
            
        Returns:
            Tuple of (chunks_created, profiles_created)
        """
        chunks_created = 0
        profiles_created = 0
        
        # Get the text content from the book
        with open(book.file.path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Create chunks using the AI workflow's text splitter
        chunks = self.chunker.chunk_text_arabic_optimized(text)
        
        # Store chunks in Django models
        with transaction.atomic():
            for idx, chunk_text in enumerate(chunks):
                chunk_obj = Chunk.objects.create(
                    book=book,
                    chunk_index=idx,
                    chunk_text=chunk_text
                )
                chunks_created += 1
                
                # Create sample profiles for each chunk (in real implementation, this would come from AI)
                # For now, we'll create a placeholder profile
                profile = Profile.objects.create(
                    chunk=chunk_obj,
                    name=f"Character_{idx}",
                    hint=f"Character from chunk {idx}",
                    age="",
                    role="",
                    personality="",
                    physical_characteristics=[],
                    events=[],
                    relationships=[],
                    aliases=[]
                )
                profiles_created += 1
        
        return chunks_created, profiles_created
    
    def get_book_profiles(self, book: Book) -> List[Profile]:
        """
        Get all profiles for a book.
        
        Args:
            book: The Book instance
            
        Returns:
            List of Profile instances for the book
        """
        return Profile.objects.filter(chunk__book=book).select_related('chunk')
    
    def get_chunk_profiles(self, chunk: Chunk) -> List[Profile]:
        """
        Get all profiles for a specific chunk.
        
        Args:
            chunk: The Chunk instance
            
        Returns:
            List of Profile instances for the chunk
        """
        return Profile.objects.filter(chunk=chunk)
    
    def get_book_chunks(self, book: Book) -> List[Chunk]:
        """
        Get all chunks for a book.
        
        Args:
            book: The Book instance
            
        Returns:
            List of Chunk instances for the book
        """
        return Chunk.objects.filter(book=book).order_by('chunk_index')
    
    def delete_book_analysis(self, book: Book):
        """
        Delete all chunks and profiles for a book.
        
        Args:
            book: The Book instance
        """
        Profile.objects.filter(chunk__book=book).delete()
        Chunk.objects.filter(book=book).delete()
    
    def get_book_analysis_summary(self, book: Book) -> Dict[str, Any]:
        """
        Get a summary of the book analysis.
        
        Args:
            book: The Book instance
            
        Returns:
            Dictionary with analysis summary
        """
        chunks = self.get_book_chunks(book)
        profiles = self.get_book_profiles(book)
        
        # Get unique characters
        unique_characters = set(profile.name for profile in profiles)
        
        return {
            'book_id': book.id,
            'book_title': book.title,
            'total_chunks': chunks.count(),
            'total_profiles': profiles.count(),
            'unique_characters': len(unique_characters),
            'character_names': list(unique_characters),
            'has_analysis': chunks.exists()
        } 