from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

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
    travel_distance = models.IntegerField()
    travel_time = models.TimeField()
    date_created = models.DateField('Date traveled')
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('detail', kwargs={'route_id': self.id})


class Photo(models.Model):
    url = models.CharField(max_length=200)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    def __str__(self):
        return f"Photo for route_id: {self.route_id} @{self.url}"