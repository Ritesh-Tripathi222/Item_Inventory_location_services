from django.db import models
from item.models import Item
from location.models import Location

# Create your models here.


class Inventory(models.Model):
    """ Inventory Model Class Attributes """
    item = models.ForeignKey(Item, models.DO_NOTHING)
    location = models.ForeignKey(Location, models.DO_NOTHING)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    quantity_unit = models.CharField(max_length=20)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    updated_by_id = models.IntegerField(blank=True, null=True)
    updated_by_role = models.CharField(max_length=20)
    status_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventory'


class InventoryAttributeSettings(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=5)
    status_code = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'inventory_attribute_settings'


class InventoryAttributeInfo(models.Model):
    inventory = models.ForeignKey('Inventory', models.DO_NOTHING)
    inventory_attribute = models.ForeignKey('InventoryAttributeSettings', models.DO_NOTHING)
    inventory_attribute_value = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'inventory_attribute_info'



