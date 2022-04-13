from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,PasswordChangeForm
# Create your views here.
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_http_methods,require_POST,require_safe
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm
from django.contrib.auth import update_session_auth_hash,get_user_model
from .forms import CustomUserCreationForm



@require_http_methods(['GET','POST'])
def login(request) :
    # 로그인 되어있으면 로그인 못하게 
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST' :
        #AuthenticationForm은 첫번째 인자로 request를 바음 
        form = AuthenticationForm(request,request.POST)
        if form.is_valid() :
            #인증이 되었다면 로그인 진행
            user = form.get_user()
            auth_login(request,user)
            return redirect(request.GET.get('next') or 'articles:index')
    
    else :
        #장고의 built-in login_form
        form = AuthenticationForm()

    context = {
        'form' : form,
    }
    return render(request,'accounts/login.html',context)


@require_POST
def logout(request):
    if request.user.is_authenticated : 
        auth_logout(request)
    return redirect('articles:index')

@require_http_methods(['GET','POST'])
def signup(request) :
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST' :
        form=CustomUserCreationForm(request.POST)
        if form.is_valid() :
            user = form.save()
            auth_login(request,user)
            return redirect('articles:index')
    else :
        form = CustomUserCreationForm()
        
    context = {
        'form' :form,
    }
    return render(request, 'accounts/signup.html',context)


@require_POST
def delete(request) :
    if request.user.is_authenticated:
        #반드시 회원 탈퇴 후 로그아웃 함수 호출 
        request.user.delete()
        auth_logout(request)
    return redirect('articles:index')

@login_required
@require_http_methods(["GET","POST"])
def update(request) :
    if request.method == 'POST' :
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid() :
            form.save()
            return redirect('articles:index')
    else :
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form' : form,
    }
    return render(request,'accounts/update.html',context)

@login_required
def change_password(request) :

    if request.method == 'POST' :
        form = PasswordChangeForm(request.user,request.POST) 
        if form.is_valid() :
            form.save()
            # auth_login(request,form.save())
            update_session_auth_hash(request,form.save())
            return redirect('articles:index')
    else :
        form = PasswordChangeForm(request.user)
    
    context= {
        'form' : form,
    }

    return render(request, 'accounts/change_password.html',context)

@require_safe
def index(request) :
    User = get_user_model()
    users = User.objects.all()

    context = {
        'users':users
    }
    return render(request,'accounts/index.html',context)