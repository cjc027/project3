from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

# Add the following import
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required # for function definitions, not CBV
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid
import boto3
from .models import Route, Photo
from .forms import RouteForm

BUCKET = 'cjc027-catcollector'
S3_BASE_URL = 'https://s3.us-west-1.amazonaws.com/'

def home(request):
	return redirect('about')
  # return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')

def about(request):
    return render(request, 'about.html')

# class RouteList(LoginRequiredMixin, ListView):
# 	model = Route

@login_required
def index(request):
	routes = Route.objects.all()
	# routes = Route.objects.filter(user=request.user)

	return render(request, 'routes/index.html', {
		'routes': routes
	})


def routes_detail(request, route_id):
    route = Route.objects.get(id=route_id)

    return render(request, 'routes/detail.html', {
        'route': route,
    })

def signup(request):
	error_message = ''

	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('index')
		else:
			error_message = 'Invalid sign up - Try again'
	
	form = UserCreationForm()
	context = {'form': form, 'error_message': error_message}
	return render(request, 'registration/signup.html', context)

class RouteCreate (CreateView):
    model = Route
    fields = fields = ['name', 'mode_of_transport', 'travel_distance', 'country', 'state', 'city', 'travel_hours', 'travel_minutes',  'description'] # referring the models field, so what fields do you want
    # to include on the form

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)

class RouteUpdate(UpdateView):
    model = Route
    # limit the renaming of the cat
    fields = ['name', 'mode_of_transport', 'travel_distance', 'country', 'state', 'city', 'travel_hours', 'travel_minutes',  'description']

class RouteDelete(DeleteView):
    model = Route
    success_url = '/routes/'


def add_photo(request, route_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, route_id=route_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', route_id=route_id)


def search(request):
	# print(request.QUERY)
	return render(request, 'search.html')

def search_index(request):
	print(request.GET, '<===== REQUEST')
	# if request.GET['city']:
	# 	print('Truthy')
	# route = Route.objects.all()
	# # print(route[0].country, '<==== 1ST ROUTE')
	# for route in Route.objects.all():
	# 	print(route.country, '<==== ROUTE.COUNTRY')
	# country = request.GET['country']
	# state = request.GET['state']
	# city = request.GET['city']

	route_filter = {'country': '', 'state': '', 'city': ''}

	
	if request.GET['country']:
		route_filter['country'] = request.GET["country"]
	else:
		route_filter.pop('country')

	if request.GET['state']:
		route_filter['state'] = request.GET["state"]
	else:
		route_filter.pop('state')

	if request.GET['city']:
		route_filter['city'] = request.GET["city"]
	else:
		route_filter.pop('city')

	q1 = Route.objects.filter(**route_filter)


	print(q1, '<== FILTERED ROUTES')
	# q1 = Route.objects.filter(country=request.GET['country'], state=request.GET['state'], city=request.GET['city'])
	# q1 = Route.objects.filter(country=country, state=state, city=city)


	return redirect('search')