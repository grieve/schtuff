import datetime

from django.db import models
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError
from django.dispatch import receiver

from taggit.models import TaggedItemBase
from taggit.managers import TaggableManager


class Location(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Keyword(TaggedItemBase):
    content_object = models.ForeignKey("Item")


class Item(models.Model):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location)
    category = models.ManyToManyField(Category, related_name="items")
    keywords = TaggableManager(through=Keyword)

    def checked_out(self, date_from=None, date_to=None):
        if date_from is None:
            date_from = datetime.datetime.now()
        if date_to is None:
            date_to = datetime.datetime.now()

        exists = self.checkouts
        exists = exists.filter(date_from__lte=date_to)
        exists = exists.filter(date_to__gte=date_from)
        if exists.count() != 0:
            return exists.get()
        else:
            return False

    def __unicode__(self):
        return self.name


class Checkout(models.Model):
    name = models.CharField(max_length=255)
    date_from = models.DateField()
    date_to = models.DateField()
    items = models.ManyToManyField(Item, related_name="checkouts", blank=True)

    def __unicode__(self):
        return self.name


@receiver(m2m_changed)
def already_checked_out(sender, instance, action, pk_set, *args, **kwargs):
    if action != 'pre_add' or instance.__class__ != Checkout:
        return
    for key in pk_set:
        item = Item.objects.get(pk=key)
        exists = item.checked_out(instance.date_from, instance.date_to)
        if exists and exists != instance:
            raise ValidationError(
                "Item '{0}' is already checked out".format(item)
            )
