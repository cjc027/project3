from django.forms import ModelForm 
from .models import Route


class RouteForm(ModelForm):
	#Meta describes data about the functionality 

	class Meta:
		model = Route
		fields = ['country', 'state', 'city']