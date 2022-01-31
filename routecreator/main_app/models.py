from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

MODE = (
    ('R', 'Running'),
    ('B', 'Biking'),
)

class Route(models.Model):
    mode_of_transport = models.CharField(
        max_length=1,
        choices=MODE,
        default=MODE[0][0]
    )
    travel_distance = models.FloatField('Miles:', validators=[MinValueValidator(0.0)])
    travel_hours = models.IntegerField(validators=[MinValueValidator(0.0)])
    travel_minutes = models.IntegerField(validators=[MinValueValidator(0.0)])
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField('Describe your route in detail:', max_length=5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('Name of route:', max_length=100, null=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('detail', kwargs={'route_id': self.id})


class Photo(models.Model):
    url = models.CharField(max_length=200)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    def __str__(self):
        return f"Photo for route_id: {self.route_id} @{self.url}"