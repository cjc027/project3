from django.forms import ModelForm 
from .models import Route, Comment


class RouteForm(ModelForm):
	class Meta:
		model = Route
		fields = ['country', 'state', 'city']


class CommentForm(ModelForm):
    class Meta:
        ordering = ['created_on']
        model = Comment
        fields = ['content']