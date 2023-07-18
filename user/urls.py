from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [
    path('profile',views.profile,name="profile"),
    path('profile/update/<int:id>',views.profileupdate,name="profileupdate"),
    path('events',views.eventviews,name="events"),
    path('event/<str:slug>/',views.eventdetailes,name="event"),
    path('addtocart/<int:event_id>/', views.addtocart, name='addtocart'),
    path('booknow/<int:event_id>/', views.booknow, name='booknow'),
    path('cart', views.cart, name='cart'),
    path('updatequantity/<int:cart_item_id>/', views.updatequantity, name='updatequantity'),
    path('removefromcart/<int:eventid>/', views.removefromcart, name='removefromcart'),
    path('checkout/<int:userid>/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('paymenthandler/<int:userid>/', views.paymenthandler, name='paymenthandler'),
    path('yourticket/',views.yourTicket,name = 'yourticket' ),
    path('generate_qr_and_send_email/<int:userid>',views.generate_qr_and_send_email,name = 'generate_qr_and_send_email' )
]