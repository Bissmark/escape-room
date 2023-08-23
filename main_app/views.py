import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Puzzle, Photo
from .forms import PuzzleForm

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def rooms_index(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/index.html', {
        'rooms': rooms
    })

def rooms_detail(request, room_id):
    room = Room.objects.get(id=room_id)
    return render(request, 'rooms/detail.html', {
        'room': room
    })

class RoomCreate(CreateView):
    model = Room
    fields = '__all__'

class RoomUpdate(UpdateView):
    model = Room
    fields = ['description', 'difficulty', 'players', 'duration', 'price', 'location']

class RoomDelete(DeleteView):
    model = Room
    success_url = '/rooms'

def puzzles_index(request):
    puzzles = Puzzle.objects.all()
    return render(request, 'puzzles/index.html', {
        'puzzles': puzzles
    })

def puzzles_detail(request, puzzle_id):
    puzzle = Puzzle.objects.get(id=puzzle_id)
    return render(request, 'puzzles/detail.html', {
        'puzzle': puzzle
    })

class PuzzleCreate(CreateView):
    model = Puzzle
    fields = ['name', 'description', 'difficulty']

class PuzzleUpdate(UpdateView):
    model = Puzzle
    fields = ['description', 'difficulty']

class PuzzleDelete(DeleteView):
    model = Puzzle
    success_url = '/puzzles'

def puzzles_index(request):
    puzzles = Puzzle.objects.all()
    return render(request, 'puzzles/index.html', {
        'puzzles': puzzles
    })

def puzzles_detail(request, puzzle_id):
    puzzle = Puzzle.objects.get(id=puzzle_id)
    return render(request, 'puzzles/detail.html', {
        'puzzle': puzzle
    })

def add_puzzle(request, room_id):
    form = PuzzleForm(request.POST)
    if form.is_valid():
        new_puzzle = form.save(commit=False)
        new_puzzle.room_id = room_id
        new_puzzle.save()
    return redirect('detail', room_id=room_id)

def add_photo(request, room_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to room_id or room (if you have a room object)
            Photo.objects.create(url=url, room_id=room_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', room_id=room_id)

def signup(request):
    error_message = ''
    if request.method == 'POST': # if the form has been submitted
        form = UserCreationForm(request.POST) # instantiate UserCreationForm with data from request.POST
        if form.is_valid(): # check if the form is valid
            user = form.save() # save the new user to the db
            login(request, user) # log the user in
            return redirect('index') # redirect to the index page
        else:
            error_message = 'Invalid sign up - try again'
    # if the form hasn't been submitted, or there are errors, render the form template with error_message as context
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)