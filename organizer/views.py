from django.shortcuts import render,redirect
from organizer.models import Eventdetails, Ticket,Organizer
from user.models import Userprofile
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from . import urls
import secrets

# Create your views here.
def home(request):
    return render(request,"home.html")
def loginpage(request):
    return render(request,"auth.html")


def user_registration(request): 
    if request.method == 'POST':
        username = request.POST['username']
        useremail = request.POST['useremail']
        password = request.POST['password']
        conform_password = request.POST['conform_Password']
        existing_user = User.objects.filter(username=username).exists()
        if existing_user:
            messages.warning(request,'Username already exists')
            return redirect('loginpage')
        existing_EMAIL = User.objects.filter(email=useremail).exists()
        if existing_EMAIL:
            messages.warning(request,'Email Address already exists')
            return redirect('loginpage')
        if password != conform_password :
            messages.warning(request,"Passwords didn't match")
            return redirect('loginpage')
        conform_Password = request.POST['conform_Password']
        user = User.objects.create_user(username=username,email=useremail, password=password)
        messages.success(request, 'Your account has been created successfully!')
        Userprofile.objects.create(
            user=user,
            user_email= user.email,
            user_name = "",
            user_about = "",
            contact_number = "",
            user_weburl = "",
            user_fburl = "",
            user_twurl = "",
            user_ldurl = "",
            )
        return redirect('login')
    return render(request,'home.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request,'Wrong credentials')
            return redirect('loginpage')
    return render(request, 'auth.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Loged out successfully!')
    return redirect('home')

def organizer(request):
    if request.method == 'POST':
        userid = request.POST['user_id']
        organizer_name = request.POST['organizername']
        organizer_contact = request.POST['organizercontact']
        organizer_email = request.POST['organizeremail']
        organizer_address = request.POST['organizeraddress']
        organizer_bank_name = request.POST['organizerbankname']
        organizer_bank_branch = request.POST['organizerbankbranch']
        organizer_bank_ifsc = request.POST['organizerbankIFSC']
        organizer_bank_account = request.POST['organizerbankaccount']
        organizer_about = request.POST['organizerabout']
        user = User.objects.get(id=userid)
        organizer=Organizer(
            user=user,
            organizerName = organizer_name,
            organizerContact = organizer_contact,
            organizerEmail = organizer_email,
            organizerAddress = organizer_address,
            organizerBankName = organizer_bank_name,
            organizerBankAccount = organizer_bank_account,
            organizerBankBranch = organizer_bank_branch,
            organizerBankIFSC = organizer_bank_ifsc,
            organizerAbout = organizer_about,
             )
        organizer.save()
        messages.success(request, 'Organizer profile  has been created successfully!')
    slug =request.user.username
    return redirect("dashboard")


def organizer_update(request):
    if request.method == 'POST':
        userid = request.POST['user_id']
        organizer_name = request.POST['organizername']
        organizer_contact = request.POST['organizercontact']
        organizer_email = request.POST['organizeremail']
        organizer_address = request.POST['organizeraddress']
        organizer_bank_name = request.POST['organizerbankname']
        organizer_bank_branch = request.POST['organizerbankbranch']
        organizer_bank_ifsc = request.POST['organizerbankIFSC']
        organizer_bank_account = request.POST['organizerbankaccount']
        organizer_about = request.POST['organizerabout']
    
        user = User.objects.get(id=userid)
        try: 
            organizer = Organizer.objects.get(user=user)
            organizer.organizerName = organizer_name
            organizer.organizerContact = organizer_contact
            organizer.organizerEmail = organizer_email
            organizer.organizerAddress = organizer_address
            organizer.organizerBankName = organizer_bank_name
            organizer.organizerBankAccount = organizer_bank_account
            organizer.organizerBankBranch = organizer_bank_branch
            organizer.organizerBankIFSC = organizer_bank_ifsc
            organizer.organizerAbout = organizer_about
            organizer.save()
            messages.success(request, 'Organizer details  has been updated successfully!')
        except Organizer.DoesNotExist:
            organizer=Organizer(
            user=user,
            organizerName = organizer_name,
            organizerContact = organizer_contact,
            organizerEmail = organizer_email,
            organizerAddress = organizer_address,
            organizerBankName = organizer_bank_name,
            organizerBankAccount = organizer_bank_account,
            organizerBankBranch = organizer_bank_branch,
            organizerBankIFSC = organizer_bank_ifsc,
            organizerAbout = organizer_about,
             )
            organizer.save()
        return redirect("dashboard")
    return render(request,'pagenotfound.html')

def dashboard(request):
    user = request.user
    organizer = Organizer.objects.filter(user=user).first()
    allEvents =Eventdetails.objects.filter(eventOrganizer=organizer)
    eventSet={
             'allEvents':allEvents,
             'organizer': organizer if organizer else None,
             }
    if request.method == 'POST':
        event_name = request.POST['event_name']
        event_display = request.POST['event_dispaly_name']
        event_start_date = request.POST['event_start_date']
        event_end_date = request.POST['event_end_date']
        event_address = request.POST['event_address']
        event_city = request.POST['event_city']
        event_state = request.POST['event_state']
        event_country = request.POST['event_country']
        event_zipcode = int(request.POST['event_zipcode'])
        event_description = request.POST['event_description']
        event_image = request.FILES['event_image']
        secret_code = secrets.token_urlsafe(10)
        event = Eventdetails.objects.create(
            eventOrganizer=organizer,
            eventImage = event_image,
            eventName = event_name,
            eventDisplay = event_display,
            eventStartDate = event_start_date,
            eventEndDate = event_end_date,
            eventAddress = event_address,
            eventCity = event_city,
            eventState = event_state,
            eventCountry = event_country,
            eventZip = event_zipcode,
            eventDescription = event_description,
            eventsecreteCode = secret_code,
        )
        messages.success(request, 'Event created  successfully!')
        # Process ticket sets
        ticket_data = {}
        for key, value in request.POST.items():   
            if key.startswith('name') and value:
                ticket_id = key.replace('name', '')     
                ticket_data[ticket_id] = {
                    'name': value,
                    'price': request.POST.get(f'price{ticket_id}'),
                    'quantity':int(request.POST.get(f'quantity{ticket_id}')),
                }
        
        for ticket_id, data in ticket_data.items(): 
            ticket = Ticket.objects.create(
                event=event,
                ticketname=data['name'],
                ticketprice=data['price'],
                ticketCount=data['quantity'],
            )
        return redirect("dashboard")
    return render(request,"organizer.html",eventSet)
def Retrieve(request,slug):
    string = slug
    filter_id =""
    filter_name=""
    for char in string :
        if char.isdigit():
            filter_id+=char
        else:
            filter_name+=char
    currentEvent = Eventdetails.objects.filter(id=int(filter_id),eventName=filter_name)
    currentEventTicket =Ticket.objects.filter(event=currentEvent[0] )
    currentEventSet={'currentEvent':currentEvent,'currentEventTicket':currentEventTicket}    
    if currentEvent :
        return render(request,"update.html",currentEventSet)
    else:
        return render(request,'pagenotfound.html')

def eventdashboard(request,slug):
    string = slug
    filter_id =""
    filter_name=""
    for char in string :
        if char.isdigit():
            filter_id+=char
        else:
            filter_name+=char
    currentEvent = Eventdetails.objects.filter(id=int(filter_id),eventName=filter_name)
    currentEventTicket =Ticket.objects.filter(event=currentEvent[0] )
    currentEventSet={'currentEvent':currentEvent,'currentEventTicket':currentEventTicket}    
    return render(request,"eventstatus.html",currentEventSet)

def Update(request):
    if request.method == 'POST':
        eventid = request.POST['eventid']
        
        event_object= get_object_or_404(Eventdetails, id=eventid)
        
        event_object.eventImage = request.FILES['event_image']
        event_object.eventName = request.POST['event_name']
        event_object.eventDisplay = request.POST['event_dispaly_name']
        event_object.eventStartDate = request.POST['event_start_date']
        event_object.eventEndDate = request.POST['event_end_date']
        event_object.eventAddress = request.POST['event_address']
        event_object.eventCity = request.POST['event_city']
        event_object.eventState = request.POST['event_state']
        event_object.eventCountry = request.POST['event_country']
        event_object.eventZip = int(request.POST['event_zipcode'])
        event_object.eventDescription = request.POST['event-description']
        event_object.save()
        messages.success(request, 'Your Event has been updated successfully!')
        
        for ticketkey,value in request.POST.items():
            if ticketkey.isdigit() and value:
                ticket_id = ticketkey
                ticket_object = get_object_or_404(Ticket, id = ticket_id)
                ticket_object.ticketname = request.POST.get(f'name{ticket_id}')
                ticket_object.ticketprice = request.POST.get(f'price{ticket_id}')
                ticket_object.ticketCount = int(request.POST.get(f'quantity{ticket_id}'))
                ticket_object.save() 
        slug= str(request.POST['event_name'])+str(eventid )
        return redirect('Retrieve',slug)
    return render(request,'pagenotfound.html')
def deletevent(request,id):
    event = Eventdetails.objects.get(id=id)
    event.delete()
    messages.success(request, 'Your Event has been deleted successfully!')
    return redirect("dashboard")






