from django import template
from ..models import Category

register = template.Library()

@register.inclusion_tag('partials/show_brezili_tag.html')
def show_brezili_tag():
    qs = Category.objects.catshow()
    for cat in qs:
        if cat.name == 'گوشت برزیلی':
            cat = cat.meatcat.meatshow()
            return {'brezilicat': cat}


@register.inclusion_tag('partials/show_goosaleh_javaneh_tag.html')
def show_goosaleh_javaneh_tag():
    qs = Category.objects.catshow()
    for cat in qs:
        if cat.name == 'گوشت گوساله جوانه':
            return {'goosaleh_javaneh': cat.meatcat.meatshow()}


@register.inclusion_tag('partials/show_goosfandi_tag.html')
def show_goosfandi_tag():
    qs = Category.objects.catshow()
    for cat in qs:
        if cat.name == 'گوشت گوسفندی':
            return {'goosfandi': cat.meatcat.meatshow()}


@register.inclusion_tag('partials/show_morgh_tag.html')
def show_morgh_tag():
    qs = Category.objects.catshow()
    for cat in qs:
        if cat.name == 'گوشت مرغ':
            return {'morgh': cat.meatcat.meatshow()}