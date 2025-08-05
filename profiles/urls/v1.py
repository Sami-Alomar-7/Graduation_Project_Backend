from django.urls import path
from profiles import views

app_name = 'profiles'

urlpatterns = [
    path('list/', views.profile_list, name='profile_list'),
    path('detail/<uuid:profile_id>/', views.profile_detail, name='profile_detail'),
    path('book/<int:book_id>/summary/', views.book_profiles_summary, name='book_profiles_summary'),
    path('character/<str:character_name>/', views.character_profiles, name='character_profiles'),
] 