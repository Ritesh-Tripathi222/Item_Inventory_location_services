from django.db import models
from django.conf import settings


class Item(models.Model):
    client_id = models.IntegerField()
    name = models.CharField(max_length=50)
    sku = models.CharField(unique=True, max_length=20)
    upc = models.CharField(max_length=20)
    ean = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    barcode = models.CharField(max_length=20)
    department = models.CharField(max_length=50)
    item_class = models.CharField(max_length=50)
    unit = models.CharField(max_length=20)
    short_description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    updated_by_id = models.IntegerField(blank=True, null=True)
    updated_by_role = models.CharField(max_length=20)
    status_code = models.IntegerField(choices=settings.STATUS_CHOICES, default=1)
    item_type = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'item'


class ItemDetail(models.Model):
    item = models.ForeignKey(Item,models.DO_NOTHING)
    description = models.TextField(blank=True, null=True)
    dimension_unit = models.CharField(max_length=20, blank=True, null=True)
    dimension_x = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dimension_y = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dimension_z = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight_unit = models.CharField(max_length=20, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    lead_time = models.DecimalField(max_digits=5, decimal_places=2)
    lead_time_unit = models.CharField(max_length=20)
    protection_level = models.CharField(max_length=20)
    min_quantity = models.DecimalField(max_digits=5, decimal_places=2)
    channel_type = models.CharField(max_length=100)
    is_dropship_only = models.CharField(max_length=3)
    shipping_restrictions = models.CharField(max_length=100)
    delivery_method = models.CharField(max_length=30)
    fulfillment_types = models.CharField(max_length=100)
    shipping_service_level = models.CharField(max_length=20)
    is_returnable = models.CharField(max_length=3, blank=True, null=True)
    manufacturer = models.CharField(max_length=50)
    vendor_name = models.CharField(max_length=50)
    mpn = models.CharField(max_length=30)
    isbn = models.CharField(max_length=30)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    updated_by_id = models.IntegerField(blank=True, null=True)
    updated_by_role = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'item_detail'


class ItemPurchaseInfo(models.Model):
    item = models.ForeignKey(Item, models.DO_NOTHING)
    purchase_price_unit = models.CharField(max_length=3)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_account = models.CharField(max_length=30)
    purchase_account_id = models.CharField(max_length=30)
    purchase_description = models.CharField(max_length=100)
    purchase_tax = models.DecimalField(max_digits=5, decimal_places=2)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    updated_by_id = models.IntegerField(blank=True, null=True)
    updated_by_role = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'item_purchase_info'


class ItemSellingInfo(models.Model):
    item = models.ForeignKey(Item, models.DO_NOTHING)
    selling_price_unit = models.CharField(max_length=3)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_account = models.CharField(max_length=30)
    selling_account_id = models.CharField(max_length=30)
    sales_description = models.CharField(max_length=100)
    sales_tax = models.DecimalField(max_digits=5, decimal_places=2)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    updated_by_id = models.IntegerField(blank=True, null=True)
    updated_by_role = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'item_selling_info'

