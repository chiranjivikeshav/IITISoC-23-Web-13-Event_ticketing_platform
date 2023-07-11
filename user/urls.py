from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [
    path('profile/<str:username>',views.profile,name="profile"),
    path('profile/update/<int:id>',views.profileupdate,name="profileupdate"),
    
]