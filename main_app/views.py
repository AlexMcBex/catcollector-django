from django.shortcuts import render, redirect
from .models import Cat, Toy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .forms import FeedingForm

#temporary cats for building templates
# cats = [
#   {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry little demon', 'age': 3},
#   {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 2},
# ]
# Create your views here.

# Define the home view
def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')

def about(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'about.html')

def cats_index(request):
  cats = Cat.objects.all()
  return render(request, 'cats/index.html', { 'cats': cats })

def cats_detail(request, cat_id):
  cat = Cat.objects.get(id=cat_id)
  id_list = cat.toys.all().values_list('id')
  toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)
  feeding_form = FeedingForm()
  return render(request, 'cats/detail.html', { 'cat': cat, 'feeding_form': feeding_form , 'toys': toys_cat_doesnt_have})

  

class CatCreate(CreateView):
  model = Cat
  #fields attribute is required for a createview
  fields= '__all__'
  # fields = ['name', 'breed', 'description', 'age']
  # success_url = '/cats/{cat_id}'

class CatUpdate(UpdateView):
  model = Cat
  fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
  model = Cat
  success_url = '/cats/'

def add_feeding(request, cat_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit = False)
    new_feeding.cat_id = cat_id
    new_feeding.save()
  return redirect('detail', cat_id=cat_id)

# ToyList
class ToyList(ListView):
  model = Toy
  template_name = 'toys/index.html'

  # def get_query(self):

def assoc_toy(request, cat_id, toy_id):
  Cat.objects.get(id=cat_id).toys.add(toy_id)
  return redirect('detail', cat_id=cat_id)

def unassoc_toy(request, cat_id, toy_id):
  Cat.objects.get(id=cat_id).toys.remove(toy_id)
  return redirect('detail', cat_id=cat_id)

# ToyDetail
class ToyDetail(DetailView):
  model = Toy
  template_name = 'toys/detail.html'

# ToyCreate
class ToyCreate(CreateView):
  model = Toy
  fields = ['name', 'color']
  
  def form_valid(self, form):
    return super().form_valid(form)


# ToyUpdate
class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']


# ToyDelete
class ToyDelete(DeleteView):
  model= Toy
  success_url = '/toys/'
