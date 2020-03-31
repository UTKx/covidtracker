from django.urls import path
from django.urls import path, include

from . import views

rlpatterns = [
    path('', views.track_all),
]
