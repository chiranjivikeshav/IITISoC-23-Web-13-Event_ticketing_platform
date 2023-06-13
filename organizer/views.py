from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,"base.html")
def dashboard(request):
    return render(request,"organizer.html")