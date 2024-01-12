from django.urls import path
from .views import ShowMeats, DetailViews

app_name = 'meat'
urlpatterns = [
    path('', ShowMeats.as_view(), name='home'),
    path('<slug:slug>/', DetailViews.as_view(), name='detail-view'),


]
