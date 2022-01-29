from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('routes/', views.RouteList.as_view(), name='index'),
    path('routes/<int:route_id>/', views.routes_detail, name='detail'),
]