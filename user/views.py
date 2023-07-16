from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from user.models import Userprofile,CartItem,Attendee
from organizer.models import Eventdetails,Ticket
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.urls import reverse

def profile(request):
    user= request.user
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
    cartItem1 = CartItem.objects.filter(event=event,user=user,paymentStatus=False).first()
    if cartItem1:
        messages.success(request,"Event Already in The Cart")
        return redirect('events')
    ticketTypes = Ticket.objects.filter(event=event)
    for ticketType in ticketTypes:
        cartItem = CartItem(event=event, user=user ,ticket_type=ticketType)
        cartItem.save()
    messages.success(request,"Event Added to The Cart")
    return redirect('events')


def cart(request):
    uuSer=User.objects.get(id=request.user.id)
    cartItems = CartItem.objects.filter(user=uuSer,paymentStatus=False)
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
    return redirect('cart')

def removefromcart(request, eventid):
    user = request.user
    userid = user.id
    Event = Eventdetails.objects.get(id=eventid)
    for item in CartItem.objects.filter(user=user,paymentStatus=False):
        if item.event == Event:
            item.delete()
    return redirect('cart')


@login_required
def booknow(request, event_id):
    user = request.user
    userid = user.id
    event = Eventdetails.objects.get(pk=event_id)
    cartItem1 = CartItem.objects.filter(event=event,user=user,paymentStatus=False).first()
    if cartItem1:
        return redirect('cart')
    ticketTypes = Ticket.objects.filter(event=event)
    for ticketType in ticketTypes:
        cartItem = CartItem(event=event, user=user ,ticket_type=ticketType)
        cartItem.save()
    userid = user.id
    return redirect('cart')



@login_required
def checkout(request,userid):
    user=request.user
    cartitem=CartItem.objects.filter(user=user ,quantity__gt=0,paymentStatus=False)
    items = []
    total_cost = sum(item.ticket_type. ticketprice * item.quantity for item in cartitem)
    total_quintity = 0
    for cart_item in cartitem:
        event = cart_item.event
        ticket_type = cart_item.ticket_type
        quantity = cart_item.quantity
        total_quintity+=quantity
        for _ in range(quantity):
            items.append({
                'event': event,
                'ticket_type': ticket_type,
                'cartitem_id':cart_item.id,
            })
    if total_quintity == 0:
        messages.warning(request,"Please Update quintity")
        return redirect('cart')
    return render(request,'checkout.html',{'items': items,'cartitem':cartitem,'total_cost':int(total_cost)})



razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
def payment( request):
    if request.method == 'POST':
        user=request.user
        userid  = user.id
        cartitem=CartItem.objects.filter(user=user ,quantity__gt=0,paymentStatus=False)
        total_cost = sum(item.ticket_type. ticketprice * item.quantity for item in cartitem)
        total_quintity = 0
        for cart_item in cartitem:
            total_quintity+=cart_item.quantity
        for num in range(total_quintity):
            request.session['attendeename'+str(num+1)] = request.POST['attendeename'+str(num+1)]
            request.session['attendeeemail'+str(num+1)] = request.POST['attendeeemail'+str(num+1)]
            request.session['attendeegender'+str(num+1)] = request.POST['attendeegender'+str(num+1)]
            request.session['attendeeaddress'+str(num+1)] = request.POST['attendeeaddress'+str(num+1)]
            request.session['attendeecontact'+str(num+1)] = request.POST['attendeecontact'+str(num+1)]
            request.session['attendeecountry'+str(num+1)] = request.POST['attendeecountry'+str(num+1)]
            request.session['attendeestate'+str(num+1)] = request.POST['attendeestate'+str(num+1)]
            request.session['attendeeZIP'+str(num+1)] = request.POST['attendeeZIP'+str(num+1)]
            request.session['attendeeEventId'+str(num+1)] = request.POST['attendeeEventId'+str(num+1)]
            request.session['attendeecartItemId'+str(num+1)] = request.POST['attendeecartItemId'+str(num+1)]
            
        currency = 'INR'
        amount = int(total_cost*100)
   
        razorpay_order = razorpay_client.order.create(dict(amount=int(amount),currency=currency,payment_capture='0'))
        razorpay_order_id = razorpay_order['id']
        # callback_url = "http://" + "127.0.0.1:8000" + "/user/paymenthandler/"
        callback_url = request.build_absolute_uri(reverse('paymenthandler', args=[userid]))
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        return render(request,'payment.html',{'total_cost':int(total_cost),**context})
    return render(request,'pagenotfound.html')

@csrf_exempt
def paymenthandler(request, userid):
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            amount = request.POST.get('amount','')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
           
            if result is not None:
                user = User.objects.get(id=userid)
                cart_items = CartItem.objects.filter(user=user, quantity__gt=0, paymentStatus=False)
                total_quintity = 0
                for cart_item in cart_items:
                    total_quintity+=cart_item.quantity
                for num in range(total_quintity):
                    event__id = request.session.get('attendeeEventId'+str(num+1))
                    cartitem__id = request.session.get('attendeecartItemId'+str(num+1))
                    attendeeprofile=Attendee(
                        event = Eventdetails.objects.get(id=event__id),
                        cartitem = CartItem.objects.get(id=cartitem__id),
                        attendeName = request.session.get('attendeename'+str(num+1)),
                        attendeEmail = request.session.get('attendeeemail'+str(num+1)),
                        attendeGender = request.session.get('attendeegender'+str(num+1)),
                        attendeAddress = request.session.get('attendeeaddress'+str(num+1)),
                        attendeContact = request.session.get('attendeecontact'+str(num+1)),
                        attendeCountry = request.session.get('attendeecountry'+str(num+1)),
                        attendeState = request.session.get('attendeestate'+str(num+1)),
                        attendeZIP = request.session.get('attendeeZIP'+str(num+1)),
                        payment_id =  payment_id,  
                    )
                    attendeeprofile.save()
                cart_items.update(paymentStatus=True)
                return redirect('cart')
               
            else:
 
                # if signature verification fails.
                # return render(request, 'paymentfail.html')
                return HttpResponse("none! 2")
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
