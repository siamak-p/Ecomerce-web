from django.db import models
from djmoney.models.fields import MoneyField
from extensions.utils import jalali_converter
from django.utils.html import format_html

# from django.utils.timezone import now
# Create your models here.

class MeatManager(models.Manager):
    def meatshow(self):
        return self.filter(showed=True)


class CategoryManager(models.Manager):
    def catshow(self):
        return self.filter(showed=True)


class Category(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False, verbose_name='نام')
    slug = models.CharField(max_length=100, unique=True, blank=False, null=False, verbose_name='آدرس')
    showed = models.BooleanField(default=True, verbose_name='وضعیت نمایش')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندیها'

    def __str__(self):
        return self.name

    objects = CategoryManager()


class Meat(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='meatcat', null=True, verbose_name='دسته بندی')
    name = models.CharField(max_length=60, blank=False, null=False, verbose_name='نام')
    slug = models.CharField(max_length=100, unique=True, blank=False, null=False, verbose_name='آدرس')
    price = MoneyField(max_digits=14, decimal_places=0, default_currency='IRR', verbose_name='قیمت')
    inventory = models.PositiveIntegerField(default=0, verbose_name='موجودی به کیلو')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    image = models.ImageField(upload_to='media', verbose_name='تصویر')
    showed = models.BooleanField(default=True, verbose_name='وضعیت نمایش')
    added = models.DateTimeField(auto_now_add=True, verbose_name='زمان اضافه شدن به سیستم')
    updated = models.DateTimeField(auto_now=True, verbose_name='زمان به روز رسانی')

    class Meta:
        verbose_name = 'گوشت'
        verbose_name_plural = 'گوشتها'

    def jadded(self):
        return jalali_converter(self.added)
    jadded.short_description = 'زمان اضافه شدن به سیستم'

    def jupdated(self):
        return jalali_converter(self.updated)
    jupdated.short_description = 'زمان به روز رسانی'

    def image_thumbnail(self):
        return format_html("<img width=100 height=75 src='{}'>".format(self.image.url))
    image_thumbnail.short_description = 'تصویر'

    def __str__(self):
        return self.name

    objects = MeatManager()
