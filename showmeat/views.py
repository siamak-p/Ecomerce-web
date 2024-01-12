from django.shortcuts import render, get_object_or_404
from .models import Category, Meat
from django.views.generic import ListView, DetailView

# Create your views here.

class ShowMeats(ListView):
    # context_object_name = 'meats'
    template_name = 'home.html'
    queryset = ''


class DetailViews(DetailView):
    template_name = 'detail_view.html'
    # context_object_name = "details"

    def get_object(self):
        slug = self.kwargs.get('slug')
        global qs
        qs = get_object_or_404(Meat, slug=slug)
        # qnty = qs.productitem.get()
        # if qnty:
        #     print('quantity: ', qnty.quantity)
        # else:
        #     print('qnty is empty')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['details'] = qs
        return context
