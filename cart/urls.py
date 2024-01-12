from django.urls import path
from .views import (
    cart,
    checkout,
    add_to_cart,
    cart_update,
    checkout_add_extra_address,
    final,
    DeleteAddress,
    DeleteItem
    # checker,
    # payment_selected,
    # timing
)

app_name = 'cart'
urlpatterns = [
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('cart-update/', cart_update, name='cart-update'),
    path('extended-address/', checkout_add_extra_address, name='extended-address'),
    path('final/', final, name='final'),
    path('checkout/delete/<int:pk>', DeleteAddress.as_view(), name='delete-address'),
    path('cart/delete/<int:pk>/', DeleteItem.as_view(), name='delete-item'),
]
