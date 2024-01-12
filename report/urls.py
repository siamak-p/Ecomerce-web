from django.urls import path
from .views import tracing_order, reporting, ordering

app_name = 'report'
urlpatterns = [
    path('tracing/', tracing_order, name='tracing-order'),
    path('reporting/', reporting, name='reporting'),
    path('ordering/', ordering, name='ordering'),
]

