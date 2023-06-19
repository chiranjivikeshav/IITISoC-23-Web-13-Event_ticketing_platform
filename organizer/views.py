from django.shortcuts import render,redirect
from organizer.models import Eventdetails, Ticket
from django.shortcuts import get_object_or_404
# Create your views here.
def home(request):
    return render(request,"base.html")
def dashboard(request):
    allEvents =Eventdetails.objects.all()
    allTickets =Ticket.objects.all()
    eventSet={'allTickets':allTickets,'allEvents':allEvents}

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
        event_description = request.POST['event-description']
        
        event = Eventdetails.objects.create(
            eventName = event_name,
            eventDisplay = event_display,
            eventStartDate = event_start_date,
            eventEndDate = event_end_date,
            eventAddress = event_address,
            eventCity = event_city,
            eventState = event_state,
            eventCountry = event_country,
            eventZip = event_zipcode,
            eventDescription = event_description
        )
        
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
        print(ticket_id)
        for ticket_id, data in ticket_data.items():
            ticket = Ticket.objects.create(
                event=event,
                ticketname=data['name'],
                ticketprice=data['price'],
                ticketCount=data['quantity'],
            )
        
    return render(request,"organizer.html",eventSet)
def Retrieve(request,slug):
    string = slug
    filter_id =""
    for char in string :
        if char.isdigit():
            filter_id+=char
    currentEvent = Eventdetails.objects.filter(id=int(filter_id))
    currentEventTicket =Ticket.objects.filter(event=currentEvent[0] )
    currentEventSet={'currentEvent':currentEvent,'currentEventTicket':currentEventTicket}    
    return render(request,"update.html",currentEventSet)

def Update(request):
    if request.method == 'POST':
        eventid = request.POST['eventid']
        
        event_object = get_object_or_404(Eventdetails, id=eventid)
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
        
        
        for ticketkey,value in request.POST.items():
            if ticketkey.isdigit() and value:
                ticket_id = ticketkey
                ticket_object = get_object_or_404(Ticket, id = ticket_id)
                ticket_object.ticketname = request.POST.get(f'name{ticket_id}')
                ticket_object.ticketprice = request.POST.get(f'price{ticket_id}')
                ticket_object.ticketCount = int(request.POST.get(f'quantity{ticket_id}'))
                ticket_object.save() 
    return redirect("/organizerDashoard")

def deletevent(request,id):
    event = Eventdetails.objects.get(id=id)
    event.delete()
    return redirect("/organizerDashoard")