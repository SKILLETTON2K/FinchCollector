from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Bird, Toy
from .forms import FeedingForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def birds_index(request):
  birds = Bird.objects.all()
  return render(request, 'birds/index.html', {
    'birds': birds
  })

def birds_detail(request, bird_id):
  bird = Bird.objects.get(id=bird_id)
  # First, create a list of the toy ids that the bird DOES have
  id_list = bird.toys.all().values_list('id')
  # Query for the toys that the bird doesn't have
  # by using the exclude() method vs. the filter() method
  toys_bird_doesnt_have = Toy.objects.exclude(id__in=id_list)
  # instantiate FeedingForm to be rendered in detail.html
  feeding_form = FeedingForm()
  return render(request, 'birds/detail.html', {
    'bird': bird, 'feeding_form': feeding_form,
    'toys': toys_bird_doesnt_have
  })

def add_feeding(request, bird_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the bird_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.bird_id = bird_id
    new_feeding.save()
  return redirect('detail', bird_id=bird_id)

class BirdCreate(CreateView):
  model = Bird
  fields = ['name','family', 'description']

class BirdUpdate(UpdateView):
  model = Bird
  # Let's disallow the renaming of a bird by excluding the name field!
  fields = ['family', 'description']

class BirdDelete(DeleteView):
  model = Bird
  success_url = '/birds'

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys'

def assoc_toy(request, bird_id, toy_id):
  Bird.objects.get(id=bird_id).toys.add(toy_id)
  return redirect('detail', bird_id=bird_id)

def unassoc_toy(request, bird_id, toy_id):
  Bird.objects.get(id=bird_id).toys.remove(toy_id)
  return redirect('detail', bird_id=bird_id)