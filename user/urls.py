from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [
    path('auth/',views.userauth,name='userauth'),
    path('profile/',views.personalprofile,name='personalprofile'),
     path('profile/edit/',views.editprofile,name='editprofile'),
      path('profile/pep/',views.pep,name='pep'),
      path('profile/pep/cart',views.cart,name='cart'),
]