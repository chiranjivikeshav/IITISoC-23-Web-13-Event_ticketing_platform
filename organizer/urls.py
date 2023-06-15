from django.contrib import admin
from django.urls import path
from organizer import views
urlpatterns = [
    path('',views.home,name='home'),
    path('organizerDashoard',views.dashboard,name='dashboard'),
    path('organizerDashoard/<str:slug>',views.Retrieve,name='Retrieve'),
    path('update',views.Update,name='Update'),
    path('deleteEvent/<int:id>',views.deletevent,name='deletevent')
]