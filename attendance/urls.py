from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("class<int:class_num>", views.detail, name="detail")
]
