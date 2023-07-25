tickets=Ticket.objects.all()
    for ticket in tickets:
        print(ticket.event.id)
        if ticket.event.id == int(filter_id) :
            print(ticket)