from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    difficulty = models.CharField(max_length=100)
    players = models.IntegerField()
    duration = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'room_id': self.id})
    
class Puzzle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    difficulty = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'puzzle_id': self.id})
    
class Review(models.Model):
    date = models.DateField('date published')
    rating = models.IntegerField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_rating_display()} on {self.date}"
    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for room_id: {self.room_id} @{self.url}"
