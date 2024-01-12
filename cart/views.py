from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .models import Order, OrderItem, ShippingAddress, DeliveryTimeModel, OrderItemHistory
from showmeat.models import Meat
from .forms import ShippingAddressForm
from extensions.utils import jalali_date_converter, jalali_date_converter_latin
from django.utils import timezone
from datetime import date, timedelta, datetime
from jalali_date import date2jalali, datetime2jalali
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.urls import reverse_lazy
from cart.models import ShippingAddress
from django.views.generic import DeleteView
from cart.mixins import DeleteAddressAuthorityMixin, DeleteCartAuthorityMixin
# Create your views here.



@login_required()
def cart(request):
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
        order = []

    context = {'items': items, 'order': order, 'lenitems': len(items)}
    template_name = 'cart.html'
    return render(request, template_name, context)


def add_to_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:

            prod_id = int(request.POST.get('productID'))
            qnt_from_site = int(request.POST.get('qntFromSite'))

            if qnt_from_site >= 1:
                # agar object order sakhte nashode bashad misazad
                order, create = Order.objects.get_or_create(customer=request.user, complete=False)
                if create:
                    order.save()
                item = get_object_or_404(Meat, id=prod_id)
                order_item, created = order.orderitem.get_or_create(product=item)
                if created:
                    order_item.quantity = qnt_from_site
                    order_item.save()
                    return JsonResponse({'status': "{} کیلو {} به سبد خرید اضافه شد.".format(qnt_from_site, order_item.product.name)})

                else:
                    order_item.quantity += qnt_from_site
                    order_item.save()
                    return JsonResponse({'status': "{} کیلو {} به سبد خرید اضافه شد.".format(qnt_from_site, order_item.product.name)})
            else:
                return JsonResponse({'status': "لطفا وزن مورد نیاز را مشخص فرمایید."})

        return JsonResponse({'status': "لطفا ابتدا وارد شوید."})

@login_required()
def checkout(request):
    template_name = 'checkout.html'
    # context = {}
    try:
        # o yeki az sefareshate moshtariye moshakhas ast, oi, item sefaresh dade shodeye haman moshtari ast. yani agar oi vojood dashte bashad sabade kharide moshtari por ast.
        o = Order.objects.filter(customer=request.user).last()
        oi = OrderItem.objects.filter(order=o)
        print('******************************************************************')
        print(o)
    except Exception as e:
        print('exception: ', e)

    if oi.exists():
        global tc
        dtf = date.today() + timedelta(days=1)
        dt = date.today()
        timecheck = int(datetime.now().strftime('%H'))
        dtf = date2jalali(dtf)
        dt = date2jalali(dt)
        today, _, _, _ = jalali_date_converter(timezone.localtime())
        tomorrow, _, _, _ = jalali_date_converter((timezone.localtime() + timedelta(days=1)))
        customer = request.user
        order = get_object_or_404(Order, customer=customer, complete=False)

        addressID = request.POST.get('address-id')
        sending_time = request.POST.get('timing')
        payment_method = request.POST.get('paymentmethod')
        validity = request.POST.get('form-validity')

        # agar shipping address vojood dashte bashad baraye karbare jari, if ejra mishavad
        if request.user.usershipping.exists():
            addresses = request.user.usershipping.all()
            shipping_form = ShippingAddressForm()

        # agar shipping address baraye karbare jari vojood nadashte bashad else ejra mishavad
        else:
            addresses = []
            shipping_form = ShippingAddressForm()
            if request.method == 'POST':
                # print('address: ', request.POST.get('address'))
                shipping_form = ShippingAddressForm(request.POST or None)
                if shipping_form.is_valid():
                    print('address:', request.POST.get('address'))

                    customer = request.user
                    order = order
                    address = shipping_form.cleaned_data['address']
                    province = shipping_form.cleaned_data['province']
                    city = shipping_form.cleaned_data['city']
                    zipcode = shipping_form.cleaned_data['zipcode']
                    phone = shipping_form.cleaned_data['phone']
                    shipping_address = ShippingAddress.objects.create(
                        customer=customer, order=order, address=address,
                        province=province, city=city, zipcode=zipcode,
                        phone=phone, selected=True
                    )
                    shipping_address.save()
                    addresses = request.user.usershipping.all()
                    return HttpResponseRedirect(reverse('cart:checkout'))

        # controle zamane ersal
        # agar objecte zamane ersal(DeliveryTimeModel) vojood dashte bashad if ejra mishavad
        if DeliveryTimeModel.objects.exists():
            delivery_time = DeliveryTimeModel.objects.all()
            # objecthaei ke dar jadvale DeliveryTimeModel tarikhe fardayeshan ba tarikhe emrooz yeki ya koochaktar bashad pak mishavand
            for i in delivery_time:
                if str(i.flags) <= str(dt):
                    try:
                        i.delete()
                    except:
                        pass
            if DeliveryTimeModel.objects.exists():
                # agar dar jadvale DeliveryTimeModel 1 object bashad va field day aan be tarikhe emrooz bashad shart dorst bashad.
                if len(delivery_time) == 1 and str(delivery_time.get(day=dt).day) == str(dt):
                    pass
                else:
                    # barresi mikonad kodam object be tarikhe emrooz ast anra negah midarad va baghiye ra pak mikonad
                    for j in delivery_time:
                        if str(j.day) != str(dt):
                            try:
                                j.delete()
                            except:
                                pass
                    # bad az in ke objecthaei ke sharte bala ra nadashtand pak kard barresi mikonad aya objecti hast ya na. agar bishtar az yeki bood hame ra pak mikonad ta yeki baghi bemanad
                    if DeliveryTimeModel.objects.exists():
                        delivery_time = DeliveryTimeModel.objects.all()
                        if len(delivery_time) > 1:
                            for j in delivery_time:
                                # agar yeki az flagha kamtar az 10 bashad yani az aan object estefade mishavad va bayad negah dashte shavad
                                if j.time1_flag < 10 or j.time2_flag < 10 or j.time3_flag < 10 or j.time4_flag < 10:
                                    continue
                                else:
                                    try:
                                        j.delete()
                                    except:
                                        pass
                                if len(delivery_time) == 1:
                                    continue
                    else:
                        DeliveryTimeModel.objects.create(day=dt, time1=True, time2=True, time3=True, time4=True, flags=dtf)
                        delivery_time = DeliveryTimeModel.objects.all()

            else:
                DeliveryTimeModel.objects.create(day=dt, time1=True, time2=True, time3=True, time4=True, flags=dtf)
                delivery_time = DeliveryTimeModel.objects.all()

        # agar objecte zamane ersal(DeliveryTimeModel) vojood nadashte bashad else ejra mishavad
        else:
            DeliveryTimeModel.objects.create(day=dt, time1=True, time2=True, time3=True, time4=True, flags=dtf)
            delivery_time = DeliveryTimeModel.objects.all()

        # code zir control mikonad aya hameye itemhaye morede niyaz baraye ersal baste entekhab shode ya kheyr
        # itemhaye morede niyaz baraye ersale baste shamele address, zamane ersal va nahveye pardakht ast
        # in flag control mikonad ke address az database entekhab shode ya kheyr
        addflag = False
        # agar dar form checkout addressi entekhab nashavad, barrasi mikonad aya addressi az ghabl entekhab shode ya khey. agar entekhab shode bashad, az aan estefade miknad
        if addressID is None:
            for i in addresses:
                if i.selected == True:
                    addressID = i.id
                    addflag = True
                else:
                    i.selected = True
                    i.save()
                    addressID = i.id
        # agar ersal az tarighe post bashad va yeki az fieldhaye morede niyaz vared shavad in if ejra mishavad va baghiye fieldha ra barrasi mikonad
        if (request.method == 'POST' and addressID is not None) or (request.method == 'POST' and sending_time is not None) or (request.method == 'POST' and payment_method is not None):
            if addressID is None and validity is False:
                return JsonResponse({'status': "لطفا آدرس خود را وارد نمایید."})
            # agar address dar form entekhab shode bashad dar database aan ra true va baghiye ra false mikonad
            elif addressID is not None and addflag is False:
                print('elif ')
                shipadd = ShippingAddress.objects.all()
                selected_shipadd = shipadd.get(id=addressID)
                print(selected_shipadd)
                selected_shipadd.selected = True
                selected_shipadd.save()
                for i in shipadd.all():
                    if i.id != int(addressID):
                        i.selected = False
                        i.save()
            print('sending_time', sending_time)
            if sending_time is None:
                # print('zaman ersal ra entekhab konid')
                return JsonResponse({'status': "لطفا زمان ارسال را انتخاب نمایید"})

            if payment_method is None:
                # print('raveshe ersal ra entekhab konid')
                return JsonResponse({'status': "لطفا نحوه ی پرداخت را انتخاب نمایید."})

        # global transaction_code
        transaction_code = get_random_string(15).lower()
        # agar karbar method offline ra entekhab konad if zir ejra mishavad
        if request.method == 'POST' and payment_method == 'offline-method':
            order.delivery_day = today
            order.online_method = False
            order.offline_method = True
            order.complete = True
            order.transaction_id = transaction_code
            order.save()
            tc = order.transaction_id
            if delivery_time.exists():
                # vaghti order sabt shod az tedad zamane ersal yeki kam mishavad
                deli = delivery_time.get()
                if str(sending_time) == 'time1':
                    deli.time1_flag -= 1
                    deli.save()
                    delivery_domain = '۹ تا ۱۲'
                elif str(sending_time) == 'time2':
                    deli.time2_flag -= 1
                    deli.save()
                    delivery_domain = '۱۲ تا ۱۵'
                elif str(sending_time) == 'time3':
                    deli.time3_flag -= 1
                    deli.save()
                    delivery_domain = '۱۵ تا ۱۸'
                else:
                    deli.time4_flag -= 1
                    deli.save()
                    delivery_domain = '۱۸ تا ۲۱'

                # barrasi mikonad ke aya time khali vojood darad ya kheyr
                if deli.time1_flag == 0:
                    deli.time1 = False
                if deli.time2_flag == 0:
                    deli.time2 = False
                if deli.time3_flag == 0:
                    deli.time3 = False
                if deli.time4_flag == 0:
                    deli.time4 = False
                deli.save()

            if addresses == []:
                impaddress = request.POST.get('impaddress')
                impprovince = request.POST.get('impprovince')
                impcity = request.POST.get('impcity')

                selected_address = str(impprovince) + '- ' + str(impcity) + '- ' + str(impaddress)
                print('**********************************************')
                print(selected_address)
                print('**********************************************')
            else:
                selected_address = addresses.get(id=addressID)
                selected_address = selected_address.province + '- ' + selected_address.city + '- ' + selected_address.address

            # mahsoolate sefareshdade shode dar jadvali joda zakhire mishavand va sabad khali mishavad
            # for e zir itemhaye sefaresh dade shode ra dar jadvali zakhire mikonad
            for prd in order.orderitem.all():
                order.orderhistory.create(
                    order=order,
                    item=prd.product,
                    quantity=prd.quantity,
                    delivery_time_bound=delivery_domain,
                    # address=addresses.get(id=addressID),
                    address=selected_address,
                    transaction_id=order.transaction_id
                )

            # ba for zir sabad khali mishavad
            for item in order.orderitem.all():
                item.delete()

            # dar in bakhsh karbar bayad be safhei montaghel shavad va be etela'ash beresad ke sefareshash sabt shode va be oo code peygiri dadae shavad
            return JsonResponse({'success': True, 'url': reverse('cart:final')})

        # agar karbar method online ra entekhab konad elif zir ejra mishavad
        elif request.method == 'POST' and payment_method == 'online-method':
            pass

        context = {
            'order': order,
            'addresses': addresses,
            'shipping_form': shipping_form,
            'delivery_time': delivery_time.get(),
            'today': today,
            'tomorrow': tomorrow,
            'addressid': addressID,
            'timecheck': timecheck
        }
    else:
        context = {'exists': oi.exists(), 'error': 'سبد شما خالیست و این صفحه برای شما نمایش داده نمی شود.'}

    return render(request, template_name, context)


def final(request):
    template_name = 'final.html'
    # print(transaction_code)
    global tc
    if tc:
        context = {'code': tc}
        tc = None
        return render(request, template_name, context)


def checkout_add_extra_address(request):
    if request.method == 'POST':
        shipping_form = ShippingAddressForm(request.POST or None)
        addresses = request.user.usershipping.all()
        order_ = Order.objects.get(customer=request.user, complete=False)
        address_ = request.POST.get('address')
        province_ = request.POST.get('province')
        city_ = request.POST.get('city')
        zipcode_ = request.POST.get('zipcode')
        phone_ = request.POST.get('phone')
        if shipping_form.is_valid():
            addresses.create(customer=request.user, order=order_, address=address_,
                             province=province_, city=city_, zipcode=zipcode_, phone=phone_)
            lstbool = list()
            for i in range(len(addresses) - 1):
                lstbool.append(False)
            lstbool.append(True)
            for i, address in enumerate(addresses):
                print(lstbool[i], address)
                address.selected = lstbool[i]
                address.save()
            del (lstbool)
        del (order_, address_, province_, city_, zipcode_, phone_, addresses, shipping_form)
        return redirect('/cart/checkout/')


def cart_update(request):
    prodid = int(request.POST.get('productID'))
    qntfromsite = int(request.POST.get('qntFromSite'))
    print('qntfromsite', qntfromsite)
    print('prodid in update is: ', prodid)

    if request.method == 'POST':
        if request.user.is_authenticated:
            order = get_object_or_404(Order, customer=request.user, complete=False)
            orderitem = order.orderitem.get(product=prodid)
            print('tedad orderitem', orderitem.quantity)
            print('orderitem: ', orderitem)
            # JsonResponse({'status': "پرینت شد"}, safe=False)

            if qntfromsite == 0:
                return JsonResponse({'status': 'لطفا وزن مورد نظر خود را انتخاب فرمایید.'})
            else:
                if qntfromsite < 0:
                    if (orderitem.quantity + qntfromsite) < 0:
                        return JsonResponse({'status': "وزن وارد شده بیشتر از وزن انتخاب شده است. لطفا صحیح وارد کنید."})
                    elif (orderitem.quantity + qntfromsite) == 0:
                        orderitem.delete()
                        return JsonResponse({'status': "{} از سبد کالا خذف شد.".format(orderitem)})
                        # return render(request, 'cart/cart.html')
                    else:
                        orderitem.quantity += qntfromsite
                        orderitem.save()
                        return JsonResponse({'status': "{} کیلو {} از سبد خرید کم شد.".format(abs(qntfromsite), orderitem)})
                        # return render(request, 'cart/cart.html')
                else:
                    orderitem.quantity += qntfromsite
                    orderitem.save()
                    return JsonResponse({'status': '{} کیلو {} به سبد خرید اضافه شد.'.format(qntfromsite, orderitem)})
    else:
        return JsonResponse({'status': 'لطفا ابتدا وارد شوید'})


class DeleteAddress(DeleteAddressAuthorityMixin, DeleteView):
    model = ShippingAddress
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy("cart:checkout")


class DeleteItem(DeleteCartAuthorityMixin, DeleteView):
    model = OrderItem
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('cart:cart')
