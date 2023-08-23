from django.forms import ModelForm
from .models import Puzzle, Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'difficulty', 'players', 'duration', 'location']

class PuzzleForm(ModelForm):
    class Meta:
        model = Puzzle
        fields = ['name', 'description', 'difficulty', 'room']