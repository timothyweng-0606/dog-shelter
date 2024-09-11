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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dog-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

def about(request):
    return render(request, 'about.html')

@login_required
def dog_index(request):
    status_filter = request.GET.get('status')
    if status_filter in ['N', 'A', 'I']:
        dogs = Dog.objects.filter(status=status_filter)
    else:
        dogs = Dog.objects.all()

        total_dogs = Dog.objects.filter(status__in=['N', 'I']).count()

    return render(request, 'dogs/index.html', {'dogs': dogs, 'total_dogs': total_dogs})

@login_required
def dog_detail(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    vacination_form = VacinationForm()
    return render(request, 'dogs/detail.html', {'dog': dog, 'vacination_form': vacination_form})


def add_vaccine(request, dog_id):
    form = VacinationForm(request.POST)
    if form.is_valid():
        new_vaccine = form.save(commit=False)
        new_vaccine.dog_id = dog_id
        new_vaccine.save()
    return redirect('dog-detail', dog_id=dog_id)


class DogCreate(LoginRequiredMixin,CreateView):
    model = Dog
    fields = '__all__'
    success_url = '/dogs/'
def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

class DogUpdate(LoginRequiredMixin,UpdateView):
    model = Dog
    fields = ['breed', 'description', 'age', 'status']

class DogDelete(LoginRequiredMixin,DeleteView):
    model = Dog
    success_url = '/dogs/'