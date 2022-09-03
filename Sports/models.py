from django.db import models
from Home.models import Profile

# Create your models here.

class Sport(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='sports')
    
    def __str__(self):
        return self.name

class Inventory(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.sport.name + ' - ' + self.name
    
class Review(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    review = models.TextField()

class Slot(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    availability = models.IntegerField()

    def __str__(self):
        return self.sport.name + ' - ' + self.date.strftime("%d %b") + ', ' + self.time.strftime("%I:%M %p")

class Booking(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' - ' + self.sport.name