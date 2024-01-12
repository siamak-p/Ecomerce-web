from django import forms
from django.core.validators import RegexValidator


class ShippingAddressForm(forms.Form):
    address = forms.CharField(label='آدرس', max_length=500, widget=forms.TextInput(attrs={
        'placeholder': 'آدرس*',
        'oninvalid': "this.setCustomValidity('این فیلد نمی تواند خالی باشد.')",
        'onchange': "try{setCustomValidity('')}catch(e){}",
        'id': 'address',
        'class': 'input'
    }))
    province = forms.CharField(label='استان', max_length=30, widget=forms.TextInput(attrs={
        'placeholder': 'استان*',
        'oninvalid': "this.setCustomValidity('این فیلد نمی تواند خالی باشد.')",
        'onchange': "try{setCustomValidity('')}catch(e){}",
        'id': 'province',
        'class': 'input'
    }))
    city = forms.CharField(label='شهر', max_length=30, widget=forms.TextInput(attrs={
        'placeholder': 'شهر*',
        'oninvalid': "this.setCustomValidity('این فیلد نمی تواند خالی باشد.')",
        'onchange': "try{setCustomValidity('')}catch(e){}",
        'id': 'city',
        'class': 'input'
    }))
    zipcode_regex = RegexValidator(regex=r'^\+?1?\d{10}$', message='لطفا کد پستی ۱۰ رقمی خود را صحیح وارد فرمایید.')
    zipcode = forms.CharField(validators=[zipcode_regex], label='کد پستی', widget=forms.TextInput(attrs={
        'placeholder': 'کد پستی',
        'pattern': '[0-9]{10}',
        'oninput': "setCustomValidity('')",
        # 'title':  'لطفا کد پستی ۱۰ رقمی خود را صحیح وارد فرمایید.'
        'oninvalid': "this.setCustomValidity('کد پستی خود را به صورت 10 رقمی وارد فرمایید.')",
        'id': 'zipcode',
        'class': 'input'
    }), required=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{11}$', message='لطفا شماره تماس را به صورت 09999999999 وارد فرمایید.')
    phone = forms.CharField(validators=[phone_regex], label='شماره تماس', widget=forms.TextInput(attrs={
        'placeholder': 'شماره تماس*',
        'pattern': '[0][9][0-9]{9}',
        'oninvalid': "this.setCustomValidity('لطفا شماره تماس را به صورت 09xxxxxxxxx وارد فرمایید.')",
        'onchange': "try{setCustomValidity('')}catch(e){}",
        'id': 'phone',
        'class': 'input'
    }))

