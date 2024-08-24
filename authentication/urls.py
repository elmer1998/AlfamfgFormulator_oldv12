from django.urls import path
from . import views

urlpatterns = [
    path('', views.logins, name='logins'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('in_progress_template', views.in_progress_template, name='in_progress_template'),
    path('testing', views.testing, name='testing'),

]