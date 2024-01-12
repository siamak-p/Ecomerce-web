from django.db import models
from account.models import User
from showmeat.models import Meat
from django.core.validators import RegexValidator
from datetime import date, timedelta
from jalali_date import date2jalali
from django_jalali.db import models as jmodels
from django.utils import timezone
from djmoney.models.fields import MoneyField
from extensions import utils
import datetime

# Create your models here.

today = date2jalali(date.today())
tomorrow = date2jalali((date.today() + timedelta(days=1)))


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='userorder', null=True, blank=True, verbose_name='کاربر')
    date_ordered = jmodels.jDateTimeField(default=timezone.now, max_length=30, verbose_name='زمان ثبت سفارش')
    complete = models.BooleanField(default=False, verbose_name='سفارش کامل شده؟')
    transaction_id = models.CharField(default=0, max_length=50, verbose_name='شماره پیگیری')
    delivery_day = models.CharField(max_length=30, default=0, verbose_name='روز ارسال')
    # delivery_time = models.CharField(max_length=10, default=0, verbose_name='زمان ارسال')
    online_method = models.BooleanField(default=False, verbose_name='پرداخت آنلاین')
    offline_method = models.BooleanField(default=False, verbose_name='پرداخت در محل')
    sent = models.BooleanField(default=False, verbose_name='ارسال شده؟')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def __str__(self):
        return self.customer.username

    @property
    def total_price(self):
        items = self.orderitem.all()
        total = sum(item.total_price_per_item for item in items)
        return total

    @property
    def total_ordered(self):
        items = self.orderitem.all()
        total = sum(item.quantity for item in items)
        return total

    # def get_absolute_url(self):
    #     return redirect(reverse('cart:final'))


class OrderItem(models.Model):
    product = models.ForeignKey(Meat, on_delete=models.SET_NULL, related_name='productitem', null=True, blank=True, verbose_name='محصول')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name='orderitem', null=True, blank=True, verbose_name='سفارش دهنده')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='تعداد')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        verbose_name = 'محصول سفارش داده شده'
        verbose_name_plural = 'محصولات سفارش داده شده'

    def __str__(self):
        return self.product.name

    @property
    def total_price_per_item(self):
        total = self.product.price * self.quantity
        return total


class OrderItemHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name='orderhistory', null=True, blank=True, verbose_name='سفارش مربوطه')
    item = models.CharField(max_length=50, blank=True, null=True, verbose_name='محصول انتخاب شده')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='تعداد')
    delivery_time_bound = models.CharField(max_length=30, default=0, verbose_name='بازه ی زمانی ارسال')
    address = models.CharField(max_length=300, default=0, verbose_name='آدرس ارسال شذه')
    transaction_id = models.CharField(max_length=50, null=True, blank=True, verbose_name='شماره پیگیری')
    _, year, month, day = utils.jalali_date_converter(timezone.now())
    comp = year + ',' + month + ',' + day
    addedtime = models.CharField(default=comp, max_length=20, verbose_name='تاریخ ثبت سفارش')
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{11}$', message='لطفا شماره تماس را به صورت 09999999999 وارد فرمایید.')
    # phone = models.CharField(validators=[phone_regex], max_length=11, blank=True, null=True, verbose_name='شماره تماس')
    # # weight = models.CharField(max_length=15, default=0, verbose_name='وزن')
    # price = MoneyField(max_digits=14, blank=True, null=True, decimal_places=0, default_currency='IRR', verbose_name='قیمت')
    # delivery_day = models.CharField(max_length=30, blank=True, null=True, default=0, verbose_name='روز ارسال')

    class Meta:
        verbose_name = 'تاریخچه محصول سفارش داده شده'
        verbose_name_plural = 'تاریخچه محصولات سفارش داده شده'

    def __str__(self):
        return self.item


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='usershipping', null=True, blank=True, verbose_name='کاربر')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name='ordershipping', null=True, blank=True, verbose_name='سفارش')
    address = models.CharField(max_length=500, null=False, blank=False, verbose_name='آدرس')
    province = models.CharField(max_length=30, null=False, blank=False, verbose_name='استان')
    city = models.CharField(max_length=30, null=False, blank=False, verbose_name='شهر')
    zipcode = models.CharField(max_length=10, null=True, blank=True, verbose_name='کد پستی')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{11}$', message='لطفا شماره تماس را به صورت 09999999999 وارد فرمایید.')
    phone = models.CharField(validators=[phone_regex], max_length=11, blank=False, null=False, verbose_name='شماره تماس')
    selected = models.BooleanField(default=False, verbose_name='آدرس منتخب')

    class Meta:
        verbose_name = 'آدرس حمل و نقل'
        verbose_name_plural = 'آدرس های حمل و نقل'

    def __str__(self):
        return self.address


class DeliveryTimeModel(models.Model):
    day = jmodels.jDateField(default=today, max_length=30, verbose_name='روز ارسال')
    time1 = models.BooleanField(default=True, verbose_name='زمان ارسال تام اول')
    time1_flag = models.PositiveSmallIntegerField(default=10, verbose_name='کنترلر تایم اول')
    time2 = models.BooleanField(default=True, verbose_name='زمان ارسال تایم دوم')
    time2_flag = models.PositiveSmallIntegerField(default=10, verbose_name='کنترلر تایم دوم')
    time3 = models.BooleanField(default=True, verbose_name='زمان ارسال تایم سوم')
    time3_flag = models.PositiveSmallIntegerField(default=10, verbose_name='کنترلر تایم سوم')
    time4 = models.BooleanField(default=True, verbose_name='زمان ارسال تایم سوم')
    time4_flag = models.PositiveSmallIntegerField(default=10, verbose_name='کنترلر تایم چهارم')
    flags = jmodels.jDateField(default=tomorrow, max_length=30, verbose_name='فردا')

    class Meta:
        verbose_name = 'زمان ارسال'
        verbose_name_plural = 'زمانهای ارسال'

    def __str__(self):
        return str(self.day)

