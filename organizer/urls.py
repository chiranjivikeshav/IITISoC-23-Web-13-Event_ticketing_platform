from django.contrib import admin
from django.urls import path
from organizer import views
from .views import dashboard,organizer
urlpatterns = [
    path('',views.home,name='home'),
    path('loginpage',views.loginpage,name='loginpage'),
    path('register', views.user_registration, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('organizerDashboard/<str:slug>',views.dashboard,name='dashboard'),
    path('organizerDetails',views.organizer,name='organizerDetails'),
    path('organizerDetails/update',views.organizer_update,name='organizerDetailsupdate'),
    path('organizerDashboard/edit/<str:slug>',views.Retrieve,name='Retrieve'),
    path('update',views.Update,name='update'),
    path('deleteEvent/<int:id>',views.deletevent,name='deletevent')
]