from django.urls import path
from chunks import views

app_name = 'chunks'

urlpatterns = [
    path('list/', views.chunk_list, name='chunk_list'),
    path('detail/<int:chunk_id>/', views.chunk_detail, name='chunk_detail'),
    path('book/<int:book_id>/summary/', views.book_chunks_summary, name='book_chunks_summary'),
] 