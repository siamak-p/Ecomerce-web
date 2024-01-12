from django.http import Http404
from cart.models import Order


class DeleteAddressAuthorityMixin():
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        try:
            if user.usershipping.get(id=kwargs.get('pk')):
                address_count = user.usershipping.count()
                new_address = user.usershipping.values()[address_count-2]['id']
                if address_count >= 1:
                    user.usershipping.filter(id=new_address).update(selected=True)
                # return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            print(e)

        return super().dispatch(request, *args, **kwargs)


class DeleteCartAuthorityMixin():
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        order = Order.objects.get(customer=user, complete=False)
        try:
            if order.orderitem.get(id=kwargs.get('pk')):
                return super().dispatch(request, *args, **kwargs)
        except:
            raise Http404('صفحه مورد نظر پیدا نشد.')
