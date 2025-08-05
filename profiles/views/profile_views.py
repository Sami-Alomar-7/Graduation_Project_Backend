from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from profiles.models import Profile
from chunks.models import Chunk
from books.models import Book
from profiles.serializers import ProfileSerializer, ProfileListSerializer, ProfileDetailSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_list(request):
    """
    List all profiles for a specific book or chunk
    """
    book_id = request.query_params.get('book_id')
    chunk_id = request.query_params.get('chunk_id')
    
    if not book_id and not chunk_id:
        return Response(
            {'error': 'Either book_id or chunk_id parameter is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        if chunk_id:
            chunk = get_object_or_404(Chunk, id=chunk_id)
            profiles = Profile.objects.filter(chunk=chunk)
        else:
            book = get_object_or_404(Book, id=book_id)
            profiles = Profile.objects.filter(chunk__book=book)
        
        serializer = ProfileListSerializer(profiles, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_detail(request, profile_id):
    """
    Get detailed information about a specific profile
    """
    try:
        profile = get_object_or_404(Profile, id=profile_id)
        serializer = ProfileDetailSerializer(profile)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def book_profiles_summary(request, book_id):
    """
    Get a summary of profiles for a book
    """
    try:
        book = get_object_or_404(Book, id=book_id)
        profiles = Profile.objects.filter(chunk__book=book)
        
        # Get unique characters
        unique_characters = set(profile.name for profile in profiles)
        
        summary = {
            'book_id': book.id,
            'book_title': book.title,
            'total_profiles': profiles.count(),
            'unique_characters': len(unique_characters),
            'character_names': list(unique_characters),
            'has_analysis': profiles.exists(),
            'profiles': ProfileListSerializer(profiles, many=True).data
        }
        
        return Response(summary)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def character_profiles(request, character_name):
    """
    Get all profiles for a specific character across all books
    """
    try:
        profiles = Profile.objects.filter(name__icontains=character_name)
        serializer = ProfileListSerializer(profiles, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
