from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

STATUS = (
    ('N','Not Adopted'),
    ('A', 'Adopted'),
    ('I', 'Interest'),
)

# Create your models here.
class Dog(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    status = models.CharField(max_length=1, 
                              choices=STATUS, 
                              default=STATUS[0][0])
    # neutered = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # Use the 'reverse' function to dynamically find the URL for viewing this cat's details
        return reverse('dog-detail', kwargs={'dog_id': self.id})
    

class Vacination(models.Model):
    date = models.DateField()
    vacinations = models.CharField(max_length=100)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE) 

    def __str__(self):
        return f"Vacination on {self.date}"
    
    class Meta:
        ordering = ['-date']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
        # Override the help_texts to remove them
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }