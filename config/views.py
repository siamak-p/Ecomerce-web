from django.urls import reverse
from django.http import HttpResponseRedirect


def redirect_view(request):
    return HttpResponseRedirect(reverse('meat:home'))
