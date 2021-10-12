from datetime import datetime
from django.db import models

class Location(models.Model):

    STATUS_CHOICES = (
    (1, 'active'),
    (2, 'pending'),
    (3, 'inactive'),
    )

    name = models.CharField(max_length=50)
    ref_location_id = models.CharField(unique=True, max_length=20)
    location_type_id = models.IntegerField()
    timezone = models.CharField(max_length=50)
    currency = models.CharField(max_length=3)
    payment_terms = models.CharField(max_length=30)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=10)
    country_code = models.CharField(max_length=2)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField(blank=True, null=True)
    updated_by_role = models.CharField(max_length=20)
    updated_by_id = models.IntegerField(blank=True, null=True)
    status_code = models.IntegerField(blank=True, null=True,choices=STATUS_CHOICES, default=1)

    class Meta:
        managed = False
        db_table = 'location'


class LocationContactInfo(models.Model):
    location = models.ForeignKey(Location, models.DO_NOTHING)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    designation = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField(blank=True, null=True)
    updated_by_role = models.CharField(max_length=20)
    updated_by_id = models.IntegerField(blank=True, null=True)
    status_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_contact_info'


class LocationReceivingInfo(models.Model):
    location = models.ForeignKey(Location, models.DO_NOTHING)
    day = models.CharField(max_length=3, blank=True, null=True)
    receiving_start_time = models.TimeField()
    receiving_end_time = models.TimeField()
    service_level_id = models.IntegerField()
    carrier_last_pickup = models.TimeField()
    receiving_capacity = models.IntegerField()
    processing_time_unit = models.CharField(max_length=10)
    processing_time = models.DecimalField(max_digits=5, decimal_places=2)
    additional_info = models.TextField()
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField(blank=True, null=True)
    updated_by_role = models.CharField(max_length=20)
    updated_by_id = models.IntegerField(blank=True, null=True)
    status_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_receiving_info'


class LocationShippingInfo(models.Model):
    location = models.ForeignKey(Location, models.DO_NOTHING)
    day = models.CharField(max_length=3)
    shipping_start_time = models.TimeField()
    shipping_end_time = models.TimeField()
    service_level_id = models.IntegerField()
    carrier_last_pickup = models.TimeField()
    shipping_capacity = models.IntegerField()
    processing_time_unit = models.CharField(max_length=10)
    processing_time = models.DecimalField(max_digits=5, decimal_places=2)
    additional_info = models.TextField()
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField(blank=True, null=True)
    updated_by_role = models.CharField(max_length=20)
    updated_by_id = models.IntegerField(blank=True, null=True)
    status_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_shipping_info'


class LocationTypes(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    status_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_types'


class ServiceLevels(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=3)
    status_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_levels'
