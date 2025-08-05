from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from books.models import Book
from chunks.services import AIBookProcessor
from books.tasks import process_book_with_ai_task, delete_book_analysis_task


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_book_with_ai(request, book_id):
    """
    Process a book with AI to extract chunks and character profiles
    """
    try:
        book = get_object_or_404(Book, id=book_id)
        
        # Check if book has a file
        if not book.file:
            return Response(
                {'error': 'Book has no file attached'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get user email for notifications
        user_email = request.user.email if hasattr(request.user, 'email') else None
        
        # Start async task
        task = process_book_with_ai_task.delay(book_id, user_email)
        
        return Response({
            'message': 'Book processing started',
            'task_id': task.id,
            'book_id': book_id,
            'status': 'processing'
        }, status=status.HTTP_202_ACCEPTED)
            
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_book_analysis_summary(request, book_id):
    """
    Get a summary of the AI analysis for a book
    """
    try:
        book = get_object_or_404(Book, id=book_id)
        processor = AIBookProcessor()
        summary = processor.get_book_analysis_summary(book)
        return Response(summary)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_book_analysis(request, book_id):
    """
    Delete all chunks and profiles for a book
    """
    try:
        book = get_object_or_404(Book, id=book_id)
        
        # Get user email for notifications
        user_email = request.user.email if hasattr(request.user, 'email') else None
        
        # Start async task
        task = delete_book_analysis_task.delay(book_id, user_email)
        
        return Response({
            'message': 'Book analysis deletion started',
            'task_id': task.id,
            'book_id': book_id,
            'status': 'deleting'
        }, status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_status(request, task_id):
    """
    Get the status of a Celery task
    """
    try:
        from celery.result import AsyncResult
        
        task_result = AsyncResult(task_id)
        
        if task_result.ready():
            if task_result.successful():
                result = task_result.result
                return Response({
                    'task_id': task_id,
                    'status': 'completed',
                    'result': result
                })
            else:
                return Response({
                    'task_id': task_id,
                    'status': 'failed',
                    'error': str(task_result.result)
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'task_id': task_id,
                'status': 'processing'
            })
            
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 