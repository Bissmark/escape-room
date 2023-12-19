from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('rooms/', views.rooms_index, name='index'),
    path('submit/', views.submit, name='submit'),
    path('rooms/<int:room_id>/', views.rooms_detail, name='detail'),
    path('rooms/create/', views.RoomCreate.as_view(), name='rooms_create'),
    path('rooms/<int:room_id>/update/', views.RoomUpdate.as_view(), name='rooms_update'),
    path('rooms/<int:room_id>/delete/', views.RoomDelete.as_view(), name='rooms_delete'),
    path('rooms/<int:room_id>/add_puzzle/', views.add_puzzle, name='add_puzzle'),
    # path('rooms/create/add_photo/', views.add_photo, name='add_photo'),
    path('puzzles/', views.puzzles_index, name='puzzles_index'),
    path('puzzles/<int:puzzle_id>/', views.puzzles_detail, name='puzzles_detail'),
    path('puzzles/create/', views.PuzzleCreate.as_view(), name='puzzles_create'),
    path('puzzles/<int:pk>/update/', views.PuzzleUpdate.as_view(), name='puzzles_update'),
    path('puzzles/<int:pk>/delete/', views.PuzzleDelete.as_view(), name='puzzles_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]