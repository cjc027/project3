from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
import os
from .models import Favorite, Route, Photo
from .forms import RouteForm, CommentForm

BUCKET = 'cjc027-catcollector'
S3_BASE_URL = 'https://s3.us-west-1.amazonaws.com/'


def home(request):
    return redirect('about')


def about(request):
    return render(request, 'about.html')


@login_required
def index(request):
    routes = Route.objects.filter(user=request.user)
    return render(request, 'routes/index.html', {
        'routes': routes
    })


def routes_detail(request, route_id):
    key = os.environ['GOOGLE_MAPS_EMBED_API_KEY']
    route = Route.objects.get(id=route_id)
    comment_form = CommentForm()
    user_favorites = Favorite.objects.filter(route_id=route_id, user_id=request.user.id).values_list('id')
    state = route.state.replace(" ", "+")
    city = route.city.replace(" ", "+")
    return render(request, 'routes/detail.html', {
        'route': route,
        'comment_form': comment_form,
        'user_favorites': user_favorites,
        'maps_key': key,
        'state': state,
        'city': city
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


class RouteCreate (LoginRequiredMixin, CreateView):
    model = Route
    fields = fields = ['name', 'mode_of_transport', 'travel_distance', 'country', 'state', 'city',
                       'travel_hours', 'travel_minutes',  'description'] 
   

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class RouteUpdate(LoginRequiredMixin, UpdateView):
    model = Route
    fields = ['name', 'mode_of_transport', 'travel_distance', 'country',
              'state', 'city', 'travel_hours', 'travel_minutes',  'description']


class RouteDelete(LoginRequiredMixin, DeleteView):
    model = Route
    success_url = '/routes/'


def add_photo(request, route_id):
    photo_file = request.FILES.get('photo-file', None)
    if request.user == Route.objects.get(id=route_id).user:
        if photo_file:
            s3 = boto3.client('s3')
            # need a unique "key" for S3 / needs image file extension too
            key = uuid.uuid4().hex[:6] + \
                photo_file.name[photo_file.name.rfind('.'):]
            # just in case something goes wrong
            try:
                s3.upload_fileobj(photo_file, BUCKET, key)
                # build the full url string
                url = f"{S3_BASE_URL}{BUCKET}/{key}"
                Photo.objects.create(url=url, route_id=route_id)
            except:
                print('An error occurred uploading file to S3')
        return redirect('detail', route_id=route_id)
    else:
        return

@login_required
def add_comment(request, route_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.route_id = route_id
        new_comment.user_id = request.user.id
        new_comment.save()
    return redirect('detail', route_id=route_id)


def search(request):
    return render(request, 'search.html')


def search_index(request):
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

    if route_filter.keys():
        search_results = Route.objects.filter(**route_filter)
    else:
        search_results = Route.objects.all()

    return render(request, 'routes/search_index.html', {'routes': search_results})

@login_required
def favorites(request):
	favorites = Favorite.objects.select_related('route').filter(user_id=request.user.id)

	return render(request, 'favorites.html', {
		'favorites' : favorites
	})


@login_required
def set_favorite(request, route_id):
    Favorite.objects.create(user_id=request.user.id, route_id=route_id)
    return redirect('detail', route_id=route_id)


def remove_favorite(request, route_id):
	favorite = Favorite.objects.filter(user_id=request.user.id, route_id=route_id)
	favorite.delete()
	return redirect('detail', route_id=route_id)
