from django.urls import path
from . import views

urlpatterns = [

    path('signup', views.signup, name = 'signup'),
    path('login', views.login, name = 'login'),
    path('logout', views.logout, name = 'logout'),
    path('script.js', views.serve_js, name = 'serve_js'),
]