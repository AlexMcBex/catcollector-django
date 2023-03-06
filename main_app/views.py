from django.shortcuts import render, redirect
from .models import Cat, Toy, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .forms import FeedingForm
import uuid
import boto3
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
S3_BUCKET = settings.S3_BUCKET
S3_BASE_URL = settings.S3_BASE_URL

# Define the home view
def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')

def about(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'about.html')

@login_required
def cats_index(request):
  # cats = Cat.objects.all()
  cats = Cat.objects.filter(user=request.user)
  return render(request, 'cats/index.html', { 'cats': cats })

@login_required
def cats_detail(request, cat_id):
  cat = Cat.objects.get(id=cat_id)
  id_list = cat.toys.all().values_list('id')
  toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)
  feeding_form = FeedingForm()
  return render(request, 'cats/detail.html', { 'cat': cat, 'feeding_form': feeding_form , 'toys': toys_cat_doesnt_have})

  

class CatCreate(LoginRequiredMixin, CreateView):
  model = Cat
  #fields attribute is required for a createview
  fields= ['name', 'breed', 'description', 'age']
  # fields = ['name', 'breed', 'description', 'age']
  # success_url = '/cats/{cat_id}'
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class CatUpdate(LoginRequiredMixin, UpdateView):
  model = Cat
  fields = ['breed', 'description', 'age']

class CatDelete(LoginRequiredMixin, DeleteView):
  model = Cat
  success_url = '/cats/'

@login_required
def add_feeding(request, cat_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit = False)
    new_feeding.cat_id = cat_id
    new_feeding.save()
  return redirect('detail', cat_id=cat_id)

# ToyList
class ToyList(LoginRequiredMixin, ListView):
  model = Toy
  template_name = 'toys/index.html'

  # def get_query(self):

@login_required
def assoc_toy(request, cat_id, toy_id):
  Cat.objects.get(id=cat_id).toys.add(toy_id)
  return redirect('detail', cat_id=cat_id)

@login_required
def unassoc_toy(request, cat_id, toy_id):
  Cat.objects.get(id=cat_id).toys.remove(toy_id)
  return redirect('detail', cat_id=cat_id)

# ToyDetail
class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy
  template_name = 'toys/detail.html'

# ToyCreate
class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = ['name', 'color']
  
  def form_valid(self, form):
    return super().form_valid(form)


# ToyUpdate
class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']


# ToyDelete
class ToyDelete(LoginRequiredMixin, DeleteView):
  model= Toy
  success_url = '/toys/'

# add photos
@login_required
def add_photo(request, cat_id):
  #name attribute of our form
  photo_file = request.FILES.get('photo-file', None)
  # use conditional to make sure a file is present
  if photo_file:
    s3= boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, S3_BUCKET, key)
      url = f"{S3_BASE_URL}{S3_BUCKET}/{key}"
      photo = Photo(url=url, cat_id=cat_id)
      photo.save()
    except Exception as error:
      print('Error uploading photo')
      return redirect('detail', cat_id=cat_id)
  return redirect('detail', cat_id=cat_id)

def signup (request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {"form": form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)