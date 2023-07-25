# Web-13-Event_ticketing_platform

# Project Name
### Event_ticketing_platform

# Website Name
### Eventwave

# Description
Eventwave is the Portal where Events can be posted by different organizations , and tickets can be bought by the
users.


# Features
<ul>
<li>User Registration and Authentication:</li>
Users will be able to create accounts, log in, and manage their profiles. 
<li>Event Listing:</li>
Event organizers can create and manage events by providing details such as event name, date,
time, location, ticket prices, and available seats.
<li>Ticket Purchase:</li>
Users will be able to browse through the list of events, view event details, and purchase
tickets for the events they are interested in.
<li>Payment Integration:</li>
Users will be able to pay ticket fee  through razorpay payment gateway
<li>Ticket Generation:</li>
A confirmation email is sent after the successful purchase of the ticket,along with a
unique QR code that users can use for event entry.
<li>Ticket Management:</li>
Users will be able to view and manage their purchased tickets.
<li>Ticket Access:</li>
The Organizers scan the QR code tickets sent to users on the day of the event. to allow them
entry.
<li>Admin Panel:</li>
An admin panel will be implemented to manage the overall system, including event approval,
user management, and ticket sales tracking.
</ul>


# Installation
Instructions on how to install and set up your Django project locally.
  <ul>
    <li>Clone the Repository: </li>
      git clone https://github.com/mittal-ishaan/IITISoC-23-Web-13-Event_ticketing_platform.git
    <li>Create and Activate a Virtual Environment (Optional but Recommended):</li>
      cd your-django-project<br>
      python -m venv venv <br>
      source venv/bin/activate   ( On Windows, use `venv\Scripts\activate`)
    <li>Install Project Dependencies: </li>
      pip install -r requirements.txt
    <li>Set Up the Database:</li>
      If you want to uses a new database, create a new database and run the migrations to set up the database schema<br>
      python manage.py migrate
    <li>Create a Superuser (Optional):</li>
      If you want to uses Django's admin interface, create a superuser<br>
      python manage.py createsuperuser
    <li>Start the Server:</li>
      Start the Django development server to run the project locally<br>
      python manage.py runserver
  </ul>

# Usage
this Django project can use by following above instructions .You can access the admin interface at http://127.0.0.1:8000/admin/. Log in using the superuser credentials to access the admin panel..

# Contact
mail our team at eventwave642@gmail.com for any help