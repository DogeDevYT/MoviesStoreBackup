from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home.index'), #define our home page here to keep definitions at the app level
    path('about', views.about, name='home.about'),
]