from django.forms import ModelForm 
from .models import Route, Comment


class RouteForm(ModelForm):
	#Meta describes data about the functionality 

	class Meta:
		model = Route
		fields = ['country', 'state', 'city']




class CommentForm(ModelForm):
    class Meta:
        ordering = ['created_on']
        model = Comment
        fields = ['content']