from django.shortcuts import render, Http404
from showmeat.models import Meat
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse, HttpResponseRedirect
from .forms import SignupForm, UserLoginForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .models import User
from django.core.mail import EmailMessage
from django.conf import settings

from django.contrib.auth import login, authenticate
from django.urls import reverse
# Create your views here.


class Home(LoginRequiredMixin, ListView):
    context_object_name = 'meats'
    queryset = Meat.objects.all()
    template_name = 'home.html'


class Register(CreateView):
    form_class = SignupForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی حساب کاربری'
        message = render_to_string('registration/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if self.request.is_secure() else 'http'
        })
        print('token is:', account_activation_token.make_token(user))
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, from_email=settings.EMAIL_HOST_USER, to=[to_email]
        )
        email.send()
        return HttpResponse('لینک فعال سازی حساب کاربری به ایمیل شما ارسال گردید. <a href="/login" style="">ورود</a>')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        # user.is_email_verified = True
        user.save()
        # login(request, user)
        # return redirect('home')
        return HttpResponse('حساب کاربری شما با موفقیت فعال گردید. <a href="/account/login">وارد</a> شوید')
    else:
        return HttpResponse('لینک فعال سازی منقضی شده است. <a href="/account/register">مجدد امتحان کنید</a>')


def user_login_view(request):
    # msg = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return HttpResponseRedirect(reverse('meat:home'))
    return render(request, 'registration/login.html', {'form': form})

