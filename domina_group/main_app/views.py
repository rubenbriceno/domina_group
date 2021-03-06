from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Tutor, Student, Subject, Lesson
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
def index(request):
    return render(request, 'index.html')

def contact(request):
    if request.method == "POST":
        message_name = request.POST['message-name']
        message_email =request.POST['message-email']
        message = request.POST['message']

        # send email
        send_mail(
            subject = 'This is an automatic message from: ' + message_name,# subject
            message = message,# message
            from_email= message_email,# from email
            recipient_list = ['mgustavob77@gmail.com'],# to email
            fail_silently=False,
        )

        return render(request, 'contact.html', {'message_name' : message_name, 'message_email': message_email, 'message': message})
    else:
        return render(request, 'contact.html')

def login_view(request):
    if request.method =='POST':
        # try to log the user in
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p, isStudent = True)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/'+u)
                else:
                    print('The account has been disabled.')
            else:
                print('The username and/or password is incorrect.')
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print('HEY', user.username)
            return HttpResponseRedirect('/user/'+str(user))
        else:
            HttpResponse('<h1>Try Again</h1>')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

@login_required

def profile(request, username):
    user = User.objects.get(username=username)
    # lessons = Lesson.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username})
