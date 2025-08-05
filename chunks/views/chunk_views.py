from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from chunks.models import Chunk
from books.models import Book
from chunks.serializers import ChunkSerializer, ChunkListSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chunk_list(request):
    """
    List all chunks for a specific book
    """
    book_id = request.query_params.get('book_id')
    if not book_id:
        return Response(
            {'error': 'book_id parameter is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        book = get_object_or_404(Book, id=book_id)
        chunks = Chunk.objects.filter(book=book).order_by('chunk_index')
        serializer = ChunkListSerializer(chunks, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chunk_detail(request, chunk_id):
    """
    Get detailed information about a specific chunk
    """
    try:
        chunk = get_object_or_404(Chunk, id=chunk_id)
        serializer = ChunkSerializer(chunk)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def book_chunks_summary(request, book_id):
    """
    Get a summary of chunks for a book
    """
    try:
        book = get_object_or_404(Book, id=book_id)
        chunks = Chunk.objects.filter(book=book)
        
        summary = {
            'book_id': book.id,
            'book_title': book.title,
            'total_chunks': chunks.count(),
            'total_characters': sum(chunk.chunk_size for chunk in chunks),
            'has_analysis': chunks.exists(),
            'chunks': ChunkListSerializer(chunks, many=True).data
        }
        
        return Response(summary)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
