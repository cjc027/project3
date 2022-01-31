from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('routes/', views.index, name='index'),
    path('routes/<int:route_id>/', views.routes_detail, name='detail'),
    path('accounts/signup/', views.signup, name='signup'),
    path('routes/create/', views.RouteCreate.as_view(), name='routes_create'),
    path('routes/<int:pk>/update/', views.RouteUpdate.as_view(), name='routes_update'),
    path('routes/<int:pk>/delete/', views.RouteDelete.as_view(), name='routes_delete'),
    path('routes/<int:route_id>/add_photo/', views.add_photo, name='add_photo'),
]