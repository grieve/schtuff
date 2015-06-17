from django.contrib import admin
from django import forms

from . import models


class CheckoutForm(forms.ModelForm):

    class Meta:
        model = models.Checkout
        exclude = []

    def clean(self):
        if 'items' in self.cleaned_data:
            for item in self.cleaned_data['items']:
                exists = item.checked_out(
                    self.cleaned_data['date_from'],
                    self.cleaned_data['date_to']
                )
                if exists and exists != self:
                    raise forms.ValidationError(
                        "Item '{0}' already checked out".format(item)
                    )
        return self.cleaned_data


@admin.register(models.Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    form = CheckoutForm
    list_display = ['name', 'date_from', 'date_to']


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'categories', 'keywords_list']

    def categories(self, obj):
        return ", ".join([c.name for c in obj.category.all()])

    def keywords_list(self, obj):
        return ", ".join([t.name for t in obj.keywords.all()])
