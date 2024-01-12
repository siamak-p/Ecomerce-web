from django.contrib import admin
from .models import Meat, Category
# Register your models here.

admin.site.site_header = 'مدیریت قصابی کوه گوشت'

class MeatAdmin(admin.ModelAdmin):
    def make_published(self, request, queryset):
        row_updated = queryset.update(showed=True)
        if row_updated == 1:
            message_bit = 'نمایش داده شد.'
        else:
            message_bit = 'نمایش داده شدند.'
        self.message_user(request, '{} گوشت {}'.format(row_updated, message_bit))
    make_published.short_description = 'نمایش گوشتهای انتخاب شده'

    def make_drafted(self, request, queryset):
        row_updated = queryset.update(showed=False)
        if row_updated == 1:
            message_bit = 'نمایش داده نمی شود'
        else:
            message_bit = 'نمایش داده نمی شوند'
        self.message_user(request, '{} گوشت {}'.format(row_updated, message_bit))
    make_drafted.short_description = 'عدم نمایش گوشتهای انتخاب شده'


    list_display = ['category', 'name', 'slug', 'price', 'inventory', 'description', 'image_thumbnail', 'showed', 'jadded', 'jupdated']
    list_filter = ['category', 'showed']
    search_fields = ('category', 'name', 'price')
    # prepopulated_fields = {'slug':('name',)}
    ordering = ['-updated', '-added']
    actions = [make_published, make_drafted]

admin.site.register(Meat, MeatAdmin)


class MeatCategory(admin.ModelAdmin):
    def make_published(self, request, queryset):
        row_updated = queryset.update(showed=True)
        if row_updated == 1:
            message_bit = 'نمایش داده شد'
        else:
            message_bit = 'نمایش داده شدند'
        self.message_user(request, '{} دسته بندی {}'.format(row_updated, message_bit))
    make_published.short_description = 'نمایش دسته بندی های انتخاب شده'

    def make_drafted(self, request, queryset):
        row_updated = queryset.update(showed=False)
        if row_updated == 1:
            message_bit = 'نمایش داده نمی شود'
        else:
            message_bit = 'نمایش داده نمی شوند'
        self.message_user(request, '{} دسته بندی {}'.format(row_updated, message_bit))
    make_drafted.short_description = 'عدم نمایش دسته بندی های انتخاب شده'


    list_display = ['name', 'slug', 'showed']
    actions = [make_published, make_drafted]
    # prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, MeatCategory)