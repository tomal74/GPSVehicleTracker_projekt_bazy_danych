from django.urls import path
from . import views

urlpatterns = [
    path('index.html/', views.index, name='index'),
    path('index.html/<int:id>', views.index_no, name='indeno'),
    path('', views.index_redirect, name='index_redirect'),
]