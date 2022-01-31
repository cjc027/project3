from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

# Add the following import
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required # for function definitions, not CBV
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Route, Photo


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
