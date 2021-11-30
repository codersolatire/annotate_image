from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from anotate.models import Images, Project, Users
from .models import *
from django.contrib.auth.hashers import make_password

# Create your views here.

def index(request):
    if 'user_id' not in request.session:
        return redirect(login)
    else:
        if request.method == "POST":
            files = request.FILES.getlist('traffic_images')
            print(files)

            for f in files:
                images_data = Images()
                images_data.image = f
                images_data.user = Users.objects.get(user_id=request.session['user_id'])
                images_data.save()
            
            return HttpResponse("200")
        else:
            images_data = Images.objects.filter(user=Users.objects.get(user_id=request.session['user_id']))

            return render(request ,'index.html',{'images_data':images_data})

def register(request):
    if request.method == "POST":
        users_data = Users()
        users_data.user_name = request.POST['username']
        users_data.password = make_password(request.POST['password'], "SmartCow", hasher="pbkdf2_sha256")
        users_data.save()

        project_data = Project()
        project_data.project_name = request.POST['projectname']
        project_data.project_user = Users.objects.get(user_id=users_data.pk)
        project_data.save()

        return redirect(login)
    else:
        return render(request, 'register.html',{})

def login(request):
    if request.method == "POST":
        users_data = Users.objects.filter(user_name=request.POST['username'], password=make_password(request.POST['password'], "SmartCow", hasher="pbkdf2_sha256"))

        if len(users_data) > 0:
            request.session['user_id'] = users_data[0].user_id
            return redirect(index)
        else:
            return redirect(login)
    else:
        return render(request, 'login.html',{})

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    
    return redirect(login)