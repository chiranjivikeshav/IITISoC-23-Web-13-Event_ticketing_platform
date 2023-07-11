from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from user.models import Userprofile

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



# Create your views here.
# Create your views here.
