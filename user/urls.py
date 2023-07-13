from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [
    path('profile/<str:username>',views.profile,name="profile"),
    path('profile/update/<int:id>',views.profileupdate,name="profileupdate"),
    path('events',views.eventviews,name="events"),
    path('addtocart/<int:event_id>/', views.addtocart, name='addtocart'),
    path('cart/<int:userid>', views.cart, name='cart'),
    path('updatequantity/<int:cart_item_id>/', views.updatequantity, name='updatequantity'),
    path('removefromcart/<int:eventid>/', views.removefromcart, name='removefromcart'),
]