from django import forms
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserChangeForm(UserChangeForm) :

    class Meta :
        #USER Class
        model = get_user_model()
        fields = ('email','first_name','last_name')


class CustomUserCreationForm(UserCreationForm) :

    class Meta :
        # 현재 장고 프로젝트에서 활성화된 유저
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email',)

