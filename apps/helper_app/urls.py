from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dash),
    path('description/<id>', views.description),
    path('edit/<id>', views.edit),
    path('update/<id>', views.update),
    path('delete/<id>', views.delete),
    path('add', views.add),
    path('create', views.create)

]
