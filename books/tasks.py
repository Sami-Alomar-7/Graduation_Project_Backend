from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from books.models import Book
from chunks.services import AIBookProcessor
import logging

logger = logging.getLogger(__name__)


def send_notification_email(subject, message, user_email):
    """
    Safely send notification email with proper error handling
    """
    if not user_email:
        return
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=True,
        )
        logger.info(f"Notification email sent successfully to {user_email}")
    except Exception as e:
        logger.warning(f"Failed to send notification email to {user_email}: {str(e)}")
        # Don't raise the exception - we don't want email failures to break the task


@shared_task
def process_book_with_ai_task(book_id: int, user_email: str = None):
    """
    Celery task to process a book with AI workflow.
    
    Args:
        book_id: The ID of the book to process
        user_email: Optional email to notify when processing is complete
    """
    try:
        # Get the book
        book = Book.objects.get(id=book_id)
        
        # Initialize AI processor
        processor = AIBookProcessor()
        
        # Process the book
        result = processor.process_book(book)
        
        if result['success']:
            # Send success notification
            send_notification_email(
                subject=f'Book Analysis Complete: {book.title}',
                message=f'''
                Your book "{book.title}" has been successfully processed with AI.
                
                You can now view the analysis through the API.
                ''',
                user_email=user_email
            )
            
            return {
                'success': True,
                'message': f'Book "{book.title}" processed successfully',
                'chunks_created': result.get('chunks_created', 0),
                'profiles_created': result.get('profiles_created', 0)
            }
        else:
            # Send error notification
            send_notification_email(
                subject=f'Book Analysis Failed: {book.title}',
                message=f'''
                There was an error processing your book "{book.title}".
                
                Error: {result.get('error', 'Unknown error')}
                
                Please try again or contact support.
                ''',
                user_email=user_email
            )
            
            return {
                'success': False,
                'message': f'Failed to process book "{book.title}"',
                'error': result.get('error', 'Unknown error')
            }
            
    except Book.DoesNotExist:
        return {
            'success': False,
            'message': f'Book with ID {book_id} not found',
            'error': 'Book not found'
        }
    except Exception as e:
        # Send error notification
        send_notification_email(
            subject=f'Book Analysis Error: {book_id}',
            message=f'''
            An unexpected error occurred while processing book ID {book_id}.
            
            Error: {str(e)}
            
            Please contact support for assistance.
            ''',
            user_email=user_email
        )
        
        return {
            'success': False,
            'message': f'Unexpected error processing book {book_id}',
            'error': str(e)
        }


@shared_task
def delete_book_analysis_task(book_id: int, user_email: str = None):
    """
    Celery task to delete all chunks and profiles for a book.
    
    Args:
        book_id: The ID of the book
        user_email: Optional email to notify when deletion is complete
    """
    try:
        # Get the book
        book = Book.objects.get(id=book_id)
        
        # Initialize AI processor
        processor = AIBookProcessor()
        
        # Delete the analysis
        processor.delete_book_analysis(book)
        
        # Send success notification
        send_notification_email(
            subject=f'Book Analysis Deleted: {book.title}',
            message=f'''
            The AI analysis for book "{book.title}" has been successfully deleted.
            
            All chunks and character profiles have been removed.
            ''',
            user_email=user_email
        )
        
        return {
            'success': True,
            'message': f'Analysis for book "{book.title}" deleted successfully'
        }
        
    except Book.DoesNotExist:
        return {
            'success': False,
            'message': f'Book with ID {book_id} not found',
            'error': 'Book not found'
        }
    except Exception as e:
        # Send error notification
        send_notification_email(
            subject=f'Book Analysis Deletion Error: {book_id}',
            message=f'''
            An error occurred while deleting analysis for book ID {book_id}.
            
            Error: {str(e)}
            
            Please contact support for assistance.
            ''',
            user_email=user_email
        )
        
        return {
            'success': False,
            'message': f'Error deleting analysis for book {book_id}',
            'error': str(e)
        } 