from .models import Order


def get_items_len(request):
    if request.user.is_authenticated:
        customer = request.user
        try:
            order = Order.objects.get(customer=customer, complete=False)
            items = order.orderitem.all()
        except:
            order = []
            items = []
    else:
        items = []
        # order = {'total_price': 0, 'total_ordered':0}
        order = []

    # context = {'items': items, 'order': order, 'lenitems': len(items)}
    context = {'lenitems': len(items)}
    return context
