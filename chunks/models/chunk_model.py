from django.db import models
from books.models import Book


class Chunk(models.Model):
    """
    Model for storing book chunks that will be processed by the AI workflow.
    Each chunk represents a portion of the book text that will be analyzed
    for character extraction and profile creation.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chunks')
    chunk_index = models.IntegerField(help_text="The sequential index of this chunk in the book")
    chunk_text = models.TextField(help_text="The actual text content of this chunk")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['book', 'chunk_index']
        ordering = ['book', 'chunk_index']
        indexes = [
            models.Index(fields=['book', 'chunk_index']),
            models.Index(fields=['chunk_index']),
        ]

    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.book.title}"

    @property
    def chunk_size(self):
        """Return the size of the chunk in characters"""
        return len(self.chunk_text)
