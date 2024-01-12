from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("این آدرس ایمیل وجود دارد.")
        return email


class UserLoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری', widget=forms.TextInput(attrs={
        'oninvalid': "this.setCustomValidity('این فیلد نمی تواند خالی باشد.')",
        'onchange': "try{setCustomValidity('')}catch(e){}",
    }))
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={
        "type": "Password",
        'oninvalid': "this.setCustomValidity('این فیلد نمی تواند خالی باشد.')",
        'onchange': "try{setCustomValidity('')}catch(e){}",
    }))
    captcha = CaptchaField(label='کد امنیتی')

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = None
        if username and password:
            user_qs = User.objects.filter(username=username)
            if len(user_qs) == 1:
                user = user_qs.first()
            if not user:
                raise ValidationError("حساب کاربری با این نام کاربری وجود ندارد.")
            if not user.check_password(password):
                raise ValidationError("رمز عبور اشتباه است.")
            if not user.is_active:
                raise ValidationError("حساب کاربری شما فعال نمی باشد. لطفا از لینک ارسال شده به ایمیلتان استفاده نمایید. در صورت منقضی شدن لینک, با پشتیبانی تماس حاصل نمایید.")
            return super(UserLoginForm, self).clean(*args, **kwargs)
