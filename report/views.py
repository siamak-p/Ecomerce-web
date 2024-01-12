from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from cart.models import Order, OrderItemHistory, ShippingAddress
from django.urls import reverse
from django.http import JsonResponse
from django.core import serializers
from django.utils import timezone
from extensions import utils
from django.db.models import Q
from django.contrib.auth.decorators import permission_required



# Create your views here.


# in tabe code peygiri ra gerefte va  mahsoolate sefaresh dade shodeye marboot be aan code peygiri ra bar migardanad
def tracing_order(request):
    template_name = 'tracing_order.html'
    context = {}

    if request.method == 'POST':
        search = request.POST.get('search-field')
        # print('search:', search)
        orderhist = OrderItemHistory.objects.filter(transaction_id=str(search))
        if orderhist:
            dict_items = dict()
            i = orderhist.first()
            full_name = i.order.customer.get_full_name()
            delivery_day = i.order.delivery_day
            if i.order.offline_method:
                method = 'پرداخت در محل'
            else:
                method = 'پرداخت آنلاین'

            # agar addressi be ordere jari montasab shode bashad if ejra mishavad vagarna else ejra mishavad
            if i.order.ordershipping.exists():
                phone = i.order.ordershipping.first().phone
            else:
                phone = ShippingAddress.objects.filter(customer=request.user, selected=True)
                phone = phone.first().phone
            if i.order.sent:
                is_it_sent = 'ارسال شده'
            else:
                is_it_sent = 'ارسال نشده'
            dict_items['full_name'] = full_name
            dict_items['delivery_day'] = delivery_day
            dict_items['method'] = method
            dict_items['phone'] = phone
            dict_items['is_it_sent'] = is_it_sent
            orderhist = serializers.serialize('json', orderhist.all())
            return JsonResponse({'success': True, 'data': orderhist, 'extra': dict_items, 'url': reverse('report:tracing-order')})
        else:
            return JsonResponse({'success': False, 'data': 'سفارشی با کد پیگیری وارد شده پیدا نشد.', 'url': reverse('report:tracing-order')})

    return render(request, template_name, context)


@permission_required('is_superuser', 'meat:home')
def reporting(request):
    template_name = 'report.html'
    context = {}
    report = {}
    lastmonth = ''

    if request.method == 'POST':
        _, year, month, day = utils.jalali_date_converter(timezone.now())
        today = year + ',' + month + ',' + day
        intday = int(day)

        monthindex = 0
        jmonths = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن',
                   'اسفند']

        for index, jmonth in enumerate(jmonths):
            if jmonths[index] == month:
                monthindex = index + 1
                if monthindex == 1:
                    lastmonth = jmonths[11]
                else:
                    lastmonth = jmonths[monthindex - 2]

        if monthindex == 1:
            nyear = int(year) - 1
        else:
            nyear = int(year)

        nmonth = jmonths[monthindex-1]

        clickedbtn = request.POST.get('clickedbtn')
        if clickedbtn == 'daily':
            report = OrderItemHistory.objects.filter(
                Q(addedtime=today)
            )

            dictphone = dict()
            try:
                addresses = ShippingAddress.objects.filter(selected=True)
                for address in addresses:
                    strname = str(address.customer)
                    dictphone[strname] = address.phone
            except Exception as e:
                print(e)

            luser = dict()
            for i, r in enumerate(report):
                luser['user{}'.format(i)] = r.order.customer.get_full_name()
            report = serializers.serialize('json', report.all())
            return JsonResponse({'success': True, 'data': report, 'extra': luser, 'phone': dictphone, 'url': reverse('report:reporting')})

            # context = {'reports': report}
        elif clickedbtn == 'weekly':
            if monthindex <= 6:
                if intday == 1:
                    day = 26
                    nmonth = lastmonth
                if intday == 2:
                    day = 27
                    nmonth = lastmonth
                if intday == 3:
                    day = 28
                    nmonth = lastmonth
                if intday == 4:
                    day = 29
                    nmonth = lastmonth
                if intday == 5:
                    day = 30
                    nmonth = lastmonth
                if intday == 6:
                    day = 31
                    nmonth = lastmonth
            else:
                if intday == 1:
                    day = 25
                    nmonth = lastmonth
                if intday == 2:
                    day = 26
                    nmonth = lastmonth
                if intday == 3:
                    day = 27
                    nmonth = lastmonth
                if intday == 4:
                    day = 28
                    nmonth = lastmonth
                if intday == 5:
                    day = 29
                    nmonth = lastmonth
                if intday == 6:
                    day = 30
                    nmonth = lastmonth
            print('current month:', nmonth)
            lastweek = str(nyear) + ',' + nmonth + ',' + day
            report = OrderItemHistory.objects.filter(
                Q(addedtime__lte=today) and Q(addedtime__gte=lastweek)
            )
            report = serializers.serialize('json', report.all())
            return JsonResponse({'success': True, 'data': report, 'extra': {}, 'url': reverse('report:reporting')})

        elif clickedbtn == 'monthly':
            lastmonth = str(nyear) + ',' + lastmonth + ',' + day
            report = OrderItemHistory.objects.filter(
                Q(addedtime__lte=today) and Q(addedtime__gte=lastmonth)
            )
            report = serializers.serialize('json', report.all())
            return JsonResponse({'success': True, 'data': report, 'extra': {}, 'url': reverse('report:reporting')})

    return render(request, template_name, context)


def ordering(request):
    template_name = 'report.html'

    if request.method == 'POST':
        timing_search = request.POST.get('timing-search')
        # ordhist = OrderItemHistory.objects.filter()
        print('timing_search:', timing_search)

    context = {}
    return render(request, template_name, context)


def error_404(request, exception):
    return render(request, '404.html')
