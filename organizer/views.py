from django.shortcuts import render,redirect
from organizer.models import Eventdetails, Ticket
# Create your views here.
def home(request):
    return render(request,"base.html")
def dashboard(request):
    if request.method == 'POST':
        event_name = request.POST['event_name']
        event_display = request.POST['event_dispaly_name']
        event_start_date = request.POST['event_start_date']
        event_end_date = request.POST['event_end_date']
        event_address = request.POST['event_address']
        event_city = request.POST['event_city']
        event_state = request.POST['event_state']
        event_country = request.POST['event_country']
        event_zipcode = request.POST['event_zipcode']
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
                    'quantity': request.POST.get(f'quantity{ticket_id}'),
                }
        
        for ticket_id, data in ticket_data.items():
            ticket = Ticket.objects.create(
                event=event,
                ticketname=data['name'],
                ticketprice=data['price'],
                ticketCount=data['quantity'],
            )
        
        
    
    return render(request,"organizer.html")
