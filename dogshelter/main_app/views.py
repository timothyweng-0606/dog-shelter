from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Dog
from .forms import VacinationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(LoginView):
    template_name = 'home.html'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('dog-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

def about(request):
    return render(request, 'about.html')

@login_required
def dog_index(request):
    # Render the dogs/index.html template with the dogs data
    dogs = Dog.objects.all()
    return render(request, 'dogs/index.html', {'dogs': dogs})

@login_required
def dog_detail(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    vacination_form = VacinationForm()
    return render(request, 'dogs/detail.html', {'dog': dog, 'vacination_form': vacination_form})


def add_vaccine(request, dog_id):
    # create a ModelForm instance using the data in request.POST
    form = VacinationForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the cat_id assigned
        new_vaccine = form.save(commit=False)
        new_vaccine.dog_id = dog_id
        new_vaccine.save()
    return redirect('dog-detail', dog_id=dog_id)


class DogCreate(LoginRequiredMixin,CreateView):
    model = Dog
    fields = '__all__'
    success_url = '/dogs/'
def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form)

class DogUpdate(LoginRequiredMixin,UpdateView):
    model = Dog
    # Let's disallow the renaming of a Dog by excluding the name field!
    fields = ['breed', 'description', 'age', 'status']

class DogDelete(LoginRequiredMixin,DeleteView):
    model = Dog
    success_url = '/dogs/'