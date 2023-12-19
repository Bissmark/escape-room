import uuid
import boto3
import os
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Puzzle, Photo
from .forms import PuzzleForm
from django.urls import reverse

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def rooms_index(request):
    rooms = Room.objects.all()
    
    for room in rooms:
        puzzles = room.puzzle_set.all()
        total_difficulty = sum(puzzle.difficulty for puzzle in puzzles)
        num_puzzles = len(puzzles)
        average_difficulty = total_difficulty / num_puzzles if num_puzzles else 0
        room.difficulty = average_difficulty

    return render(request, 'rooms/index.html', {
        'rooms': rooms
    })

def rooms_detail(request, room_id):
    room = Room.objects.get(id=room_id)
    puzzles_not_assigned = Puzzle.objects.filter(room__isnull=True)
    puzzles_room_doesnt_have = puzzles_not_assigned.exclude(id__in = room.puzzle_set.values_list('id'))
    all_puzzles = Puzzle.objects.all()

    puzzles = room.puzzle_set.all()
    total_difficulty = sum(puzzle.difficulty for puzzle in puzzles)
    num_puzzles = len(puzzles)
    average_difficulty = total_difficulty / num_puzzles if num_puzzles else 0
    room.difficulty = average_difficulty

    return render(request, 'rooms/detail.html', {
        'room': room,
        'puzzles_for_room': puzzles_room_doesnt_have,
        'all_puzzles': all_puzzles
    })

def add_puzzle(request, room_id):
    if request.method == 'POST':
        puzzle_id = request.POST.get('puzzle_id')
        try:
            puzzle = Puzzle.objects.get(id=puzzle_id)
            room = Room.objects.get(id=room_id)
            room.puzzle_set.add(puzzle)
            messages.success(request, f"Puzzle '{puzzle.name}' added to the room.")
        except Puzzle.DoesNotExist:
            messages.error(request, "Selected puzzle not found.")
        except Room.DoesNotExist:
            messages.error(request, "Selected room not found.")

    return redirect('detail', room_id=room_id)

class RoomCreate(CreateView):
    model = Room
    fields = ['name', 'description', 'players', 'duration', 'price', 'location', 'user']

class RoomUpdate(UpdateView):
    model = Room
    fields = ['description', 'difficulty', 'players', 'duration', 'price', 'location']

class RoomDelete(DeleteView):
    model = Room
    success_url = '/rooms'

def puzzles_index(request, room_id):
    puzzles = Puzzle.objects.all()
    room = Room.objects.filter(id=room_id)
    # room = Room.objects.get(id=room_id)
    print(room)
    return render(request, 'puzzles/index.html', {
        'puzzles': puzzles,
        'room': room
    })

def puzzles_detail(request, puzzle_id):
    puzzle = Puzzle.objects.get(id=puzzle_id)
    print(puzzle)
    return render(request, 'puzzles/detail.html', {
        'puzzle': puzzle
    })

class PuzzleCreate(CreateView):
    model = Puzzle
    fields = '__all__'

    def form_valid(self, form):
        # Call the parent class's form_valid method to save the puzzle
        response = super().form_valid(form)

        # Your logic to add a photo
        puzzle_id = self.object.id  # Assuming your Puzzle model has an 'id' attribute
        photo_file = self.request.FILES.get('photo-file', None)

        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            
            try:
                bucket = os.environ['S3_BUCKET']
                s3.upload_fileobj(photo_file, bucket, key)
                url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                Photo.objects.create(url=url, puzzle_id=puzzle_id)
            except Exception as e:
                print('An error occurred uploading file to S3')
                print(e)

        return response

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

def submit(request):
    if request.method == 'POST':
        values = [request.POST[f'counter-{counter}'] for counter in "abcd"]
        return HttpResponse(f'Submitted Values: {", ".join(values)}')
    else:
        return HttpResponse('Invalid Request')

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