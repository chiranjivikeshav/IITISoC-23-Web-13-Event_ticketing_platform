from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from user.models import Userprofile,CartItem
from organizer.models import Eventdetails,Ticket
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required



def profile(request,username):
    user= User.objects.get(username = username)
    profile = Userprofile.objects.get(user = user)
    return render(request,"profile.html",{'profile':profile})


def profileupdate(request,id):
    user=User.objects.get(id=id)
    if request.method == 'POST':
       user_name = request.POST['user_name'] 
       user_email = request.POST['user_email'] 
       contact_number = request.POST['contact_number'] 
       user_weburl = request.POST['user_weburl'] 
       user_fburl = request.POST['user_fburl'] 
       user_twurl = request.POST['user_twurl'] 
       user_ldurl = request.POST['user_ldurl'] 
       user_about = request.POST['user_about'] 
    try:
        profile = Userprofile.objects.get(user=user)
        profile.user_name = user_name
        profile.user_email = user_email
        profile.contact_number = contact_number
        profile.user_weburl = user_weburl
        profile.user_fburl = user_fburl
        profile.user_twurl = user_twurl
        profile.user_ldurl = user_ldurl
        profile.user_about = user_about
        profile.save()
        messages.success(request, 'Your profile  has been updated successfully!')
    except Userprofile.DoesNotExist:
        profile=Userprofile(
        user=user,
        user_name = user_name,
        user_email = user_email,
        contact_number = contact_number,
        user_weburl = user_weburl,
        user_fburl = user_fburl,
        user_twurl = user_twurl,
        user_ldurl = user_ldurl,
        user_about = user_about,
        )
        profile.save()
    user=User.objects.get(id=id)
    slug = user.username
    return redirect('profile',username=slug)

def eventviews(request):
    current_datetime = timezone.now()

    upcoming_events = Eventdetails.objects.filter(eventStartDate__gt=current_datetime)
    ongoing_events = Eventdetails.objects.filter(eventStartDate__lte=current_datetime, eventEndDate__gte=current_datetime)
    past_events = Eventdetails.objects.filter(eventEndDate__lt=current_datetime)

    context = {
        'upcoming_events': upcoming_events,
        'ongoing_events': ongoing_events,
        'past_events': past_events
    }
    return render(request,'events.html',context)

@login_required
def addtocart(request, event_id):
    user = request.user
    userid = user.id
    event = Eventdetails.objects.get(pk=event_id)
    cartItem1 = CartItem.objects.filter(event=event,user=user).first()
    if cartItem1:
        messages.success(request,"Event Already in The Cart")
        return redirect('events')
    ticketTypes = Ticket.objects.filter(event=event)
    for ticketType in ticketTypes:
        cartItem = CartItem(event=event, user=user ,ticket_type=ticketType)
        cartItem.save()
    messages.success(request,"Event Added to The Cart")
    return redirect('events')


def cart(request,userid):
    uuSer=User.objects.get(id=userid)
    cartItems = CartItem.objects.filter(user=uuSer)
    events = {}
    for cartItem in cartItems:
        event = cartItem.event
        ticketType = cartItem.ticket_type
        quantity = cartItem.quantity
        if event.id not in events:
            events[event.id] = {
                'event': event,
                'ticketTypes': []
            }
        events[event.id]['ticketTypes'].append({
            'ticketType': ticketType,
            'quantity': quantity,
            'cartitemid': cartItem.id
        })
    total_cost = sum(item.ticket_type. ticketprice * item.quantity for item in cartItems)
    return render(request, 'cart.html', {'events': events.values(), 'total_cost': total_cost})

def updatequantity(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    new_quantity = int(request.POST['quantity'])
    if new_quantity < 0:
        new_quantity = 0
    cart_item.quantity = new_quantity
    cart_item.save()
    user = request.user
    userid = user.id
    return redirect('cart',userid)

def removefromcart(request, eventid):
    user = request.user
    userid = user.id
    Event = Eventdetails.objects.get(id=eventid)
    for item in CartItem.objects.filter(user=user):
        if item.event == Event:
            item.delete()
    return redirect('cart',userid)


@login_required
def booknow(request, event_id):
    user = request.user
    userid = user.id
    event = Eventdetails.objects.get(pk=event_id)
    cartItem1 = CartItem.objects.filter(event=event,user=user).first()
    if cartItem1:
        return redirect('cart',userid)
    ticketTypes = Ticket.objects.filter(event=event)
    for ticketType in ticketTypes:
        cartItem = CartItem(event=event, user=user ,ticket_type=ticketType)
        cartItem.save()
    userid = user.id
    return redirect('cart',userid)
@login_required
def checkout(request,userid):
    user=request.user
    cartitem=CartItem.objects.filter(user=user)
    items = []

    for cart_item in cartitem:
        event = cart_item.event
        ticket_type = cart_item.ticket_type
        quantity = cart_item.quantity

        for _ in range(quantity):
            items.append({
                'event': event,
                'ticket_type': ticket_type,
            })

    return render(request, 'checkout.html', {'items': items})