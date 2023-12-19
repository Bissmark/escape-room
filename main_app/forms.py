from django.forms import ModelForm
from django import forms
from .models import Puzzle, Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'players', 'duration', 'location']

class PuzzleForm(ModelForm):
    class Meta:
        model = Puzzle
        fields = ['name', 'description', 'difficulty', 'room', 'lock']

    lock = forms.CharField(label='Type of Lock')