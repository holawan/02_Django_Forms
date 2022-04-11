from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
from django.contrib.auth import login as auth_login

def login(request) :

    if request.method == 'POST' :
        AuthenticationForm(request,request.post)
        if form.is_valid() :
            user = form.get_user()
            auth_login(request,user)
            return redirect('articles:index')
    
    else :
        form = AuthenticationForm()

    context = {
        'form' : form,
    }
    return render(request,'accounts/login.html',context)