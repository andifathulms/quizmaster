from django.urls import path, include

from . import views


app_name = "participants"

urlpatterns = [
    path('', views.index, name="index")
]
