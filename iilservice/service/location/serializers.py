from rest_framework import serializers
from .models import *
from rest_framework.serializers import ModelSerializer
from datetime import datetime

LOCATION_COL = [f.name for f in Location._meta.get_fields() if f.name not in ['location_type_id','locationcontactinfo','locationreceivinginfo','locationshippinginfo','date_created', 'date_updated', 'updated_by_id', 'updated_by_role','status_code', 'inventory']]

CONTACT_INFO = [f.name for f in LocationContactInfo._meta.get_fields() if f.name not in ['location','date_created', 'date_updated', 'updated_by_id', 'updated_by_role','status_code']]

RECEIVING_INFO = [f.name for f in LocationReceivingInfo._meta.get_fields() if f.name not in ['location','date_created', 'date_updated', 'updated_by_id', 'updated_by_role','status_code']]

SHIPPING_INFO = [f.name for f in LocationShippingInfo._meta.get_fields() if f.name not in ['location','date_created', 'date_updated', 'updated_by_id', 'updated_by_role','status_code']]


STATUS_CHOICES = (
    (1, 'active'),
    (2, 'pending'),
    (3, 'inactive'),
)


class LocationSearchSerializer(ModelSerializer):
    """ Location Serializer for search """
    class Meta:
        model = Location
        exclude = ('date_created','date_updated','updated_by_role','updated_by_id','status_code')


class LocationContactInfoSerializer(ModelSerializer):
    """ Location Contact Info Serializer """
    #location_id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=30,required=False)
    last_name = serializers.CharField(max_length=30,required=False)
    designation = serializers.CharField(max_length=30,required=False)
    phone = serializers.CharField(max_length=30,required=False)
    email = serializers.CharField(max_length=50,required=False)
    class Meta:
        model = LocationContactInfo
        #exclude = ('date_created','date_updated','updated_by_role','updated_by_id','status_code')
        fields = CONTACT_INFO


class LocationShippingInfoSerializer(ModelSerializer):
    """ Location Shipping Info Serializer """
    day = serializers.CharField(max_length=20,required=False)
    shipping_start_time = serializers.TimeField(required=False,default="00:00")
    shipping_end_time = serializers.TimeField(required=False,default="00:00")
    service_level_id = serializers.IntegerField(required=False,default=0)
    carrier_last_pickup = serializers.TimeField(required=False,default="00:00")
    shipping_capacity = serializers.IntegerField(required=False,default=0)
    processing_time_unit = serializers.CharField(max_length=10,required=False)
    processing_time = serializers.DecimalField(max_digits=5, decimal_places=2,required=False,default=0.00)
    additional_info = serializers.CharField(required=False)
    service_level = serializers.CharField(write_only = True,max_length = 20, required = False)

    class Meta:
        model = LocationShippingInfo
        fields = SHIPPING_INFO+['service_level']


class LocationReceivingInfoSerializer(ModelSerializer):
    """ Location Receiving Info Serializer """

    day = serializers.CharField(max_length=20,required=False)
    receiving_start_time = serializers.TimeField(required=False,default="00:00")
    receiving_end_time = serializers.TimeField(required=False,default="00:00")
    service_level_id = serializers.IntegerField(required=False,default=0)
    carrier_last_pickup = serializers.TimeField(required=False,default="00:00")
    receiving_capacity = serializers.IntegerField(required=False,default=0)
    processing_time_unit = serializers.CharField(max_length=10,required=False)
    processing_time = serializers.DecimalField(max_digits=5, decimal_places=2,required=False,default=0.00)
    additional_info = serializers.CharField(required=False)
    service_level = serializers.CharField(write_only=True,max_length = 20, required = False)

    class Meta:
        model = LocationReceivingInfo
        fields = RECEIVING_INFO+['service_level']


class LocationSerializer(ModelSerializer):
    """ Location Serializer with three nested serializers """
    id = serializers.IntegerField(read_only=True)
    #location_type_id = serializers.IntegerField(source='location_type_id')
    currency = serializers.CharField(max_length=20,required=False)
    payment_terms = serializers.CharField(max_length=30,required=False)
    address1 = serializers.CharField(max_length=100,required=False)
    address2 = serializers.CharField(max_length=100,required=False)
    city = serializers.CharField(max_length=30,required=False)
    state = serializers.CharField(max_length=30,required=False)
    postal_code = serializers.CharField(max_length=10,required=False)
    country_code = serializers.CharField(max_length=2,required=False)
    location_type = serializers.CharField(write_only=True,max_length=3,required=True)
    status = serializers.CharField(max_length=50, required=False,source='status_code')
    receiving_info = LocationReceivingInfoSerializer(write_only=True,required=False)
    shipping_info = LocationShippingInfoSerializer(write_only=True,required=False)
    contact_info = LocationContactInfoSerializer(write_only=True,required=False)
    class Meta:
        model = Location
        fields = ['location_type']+LOCATION_COL+['status','contact_info','receiving_info','shipping_info']

    def create(self, validated_data):
        """method to create entry in tables"""
        location_data = dict()
        contact_data = dict()
        receiving_data = dict()
        shipping_data = dict()

        validated_data['date_created'] = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

        if 'location_type' in validated_data:
            loc_code = validated_data.get('location_type')
            loc = LocationTypes.objects.get(code=loc_code)
            validated_data['location_type_id'] = loc.id
            location_data['location_type_id'] = validated_data['location_type_id']

        location_data['date_created'] = validated_data['date_created']
        contact_data['date_created'] = validated_data['date_created']
        receiving_data['date_created'] = validated_data['date_created']
        shipping_data['date_created'] = validated_data['date_created']


        for k in validated_data:
            if k in LOCATION_COL:
                location_data[k] = validated_data[k]


        location = Location.objects.create(**location_data)
        contact_data['location'] = location
        receiving_data['location'] = location
        shipping_data['location'] = location

        if 'contact_info' in validated_data:
            contact_info = validated_data.pop('contact_info')
            for k in contact_info:
                if k in CONTACT_INFO:
                    contact_data[k] = contact_info[k]
            LocationContactInfo.objects.create(**contact_data)

        if 'receiving_info' in validated_data:
            receiving_info = validated_data.get('receiving_info')
            for k in receiving_info:
                if k in RECEIVING_INFO:
                    receiving_data[k] = receiving_info[k]
                if k == "service_level":
                    service_lvl_code = receiving_info.get('service_level')
                    service_lvl_id = ServiceLevels.objects.get(name=service_lvl_code)
                    receiving_data['service_level_id'] = service_lvl_id.id
                    '''
                    if receiving_info['service_level'] == "Standard":
                        receiving_data['service_level_id'] = 1
                    elif receiving_info['service_level'] == "Expedited":
                        receiving_data['service_level_id'] = 2
                    else:
                        receiving_data['service_level_id'] = 0
                    '''
            LocationReceivingInfo.objects.create(**receiving_data)

        if 'shipping_info' in validated_data:
            shipping_info = validated_data.pop('shipping_info')
            for k in shipping_info:
                if k in SHIPPING_INFO:
                    shipping_data[k] = shipping_info[k]
                if k == "service_level":
                    service_lvl_code = shipping_info.pop('service_level')
                    service_lvl_id = ServiceLevels.objects.get(name=service_lvl_code)
                    shipping_data['service_level_id'] = service_lvl_id.id
                    '''
                    if shipping_info['service_level'] == "Standard":
                        shipping_data['service_level_id'] = 1
                    elif shipping_info['service_level'] == "Expedited":
                        shipping_data['service_level_id'] = 2
                    else:
                        shipping_data['service_level_id'] = 0
                    '''
            LocationShippingInfo.objects.create(**shipping_data)

        return location


    def update(self, instance, validated_data):
        """ method to update entry in tables """
        contact_data = validated_data.pop('contact_info')
        contacts = (instance.contact_info).all()
        contacts = list(contacts)

        receiving_data = validated_data.pop('receiving_info')
        receivingInfo = (instance.receiving_info).all()
        receivingInfo = list(receivingInfo)

        shipping_data = validated_data.pop('shipping_info')
        shippingInfo = (instance.shipping_info).all()
        shippingInfo = list(shippingInfo)

        instance.name = validated_data.get('name', instance.name)
        instance.ref_location_id = validated_data.get('ref_location_id', instance.ref_location_id)
        instance.location_type_id = validated_data.get('location_type_id', instance.location_type_id)
        instance.timezone = validated_data.get('timezone', instance.timezone)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.payment_terms = validated_data.get('payment_terms', instance.payment_terms)
        instance.address1 = validated_data.get('address1', instance.address1)
        instance.address2 = validated_data.get('address2', instance.address2)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.country_code = validated_data.get('country_code', instance.country_code)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.date_updated = validated_data.get('date_updated', instance.date_updated)
        instance.updated_by_role = validated_data.get('updated_by_role', instance.updated_by_role)
        instance.updated_by_id = validated_data.get('updated_by_id', instance.updated_by_id)
        instance.status_code = validated_data.get('status_code', instance.status_code)
        instance.save()

        for info in contact_info:
            contact = contacts.pop(0)
            contact.location_contact_info_id = info.get('location_contact_info_id', contact.location_contact_info_id)
            contact.first_name = info.get('first_name', contact.first_name)
            contact.last_name = info.get('last_name', contact.last_name)
            contact.designation = info.get('designation', contact.designation)
            contact.phone = info.get('phone', contact.phone)
            contact.email = info.get('email', contact.email)
            contact.save()

        for info2 in contact_info:
            receiving = receivingInfo.pop(0)
            receiving.location_receiving_info_id = info2.get('location_receiving_info_id', receiving.location_receiving_info_id)
            receiving.day = info2.get('day', receiving.day)
            receiving.receiving_start_time = info2.get('receiving_start_time', receiving.receiving_start_time)
            receiving.receiving_end_time = info2.get('receiving_end_time', receiving.receiving_end_time)
            receiving.service_level_id = info2.get('service_level_id', receiving.service_level_id)
            receiving.carrier_last_pickup = info2.get('carrier_last_pickup', receiving.carrier_last_pickup)
            receiving.receiving_capacity = info2.get('receiving_capacity', receiving.receiving_capacity)
            receiving.processing_time_unit = info2.get('processing_time_unit', receiving.processing_time_unit)
            receiving.processing_time = info2.get('processing_time', receiving.processing_time)

            receiving.save()

        for info3 in shipping_info:
            shipping = shippingInfo.pop(0)
            shipping.location_shipping_info_id = info3.get('location_shipping_info_id', shipping.location_shipping_info_id)
            shipping.day = info3.get('day', shipping.day)
            shipping.shipping_start_time = info3.get('shipping_start_time', shipping.shipping_start_time)
            shipping.shipping_end_time = info3.get('shipping_end_time', shipping.shipping_end_time)
            shipping.service_level_id = info3.get('service_level_id', shipping.service_level_id)
            shipping.carrier_last_pickup = info3.get('carrier_last_pickup', shipping.carrier_last_pickup)
            shipping.shipping_capacity = info3.get('shipping_capacity', shipping.shipping_capacity)
            shipping.processing_time_unit = info3.get('processing_time_unit', shipping.processing_time_unit)
            shipping.processing_time = info3.get('processing_time', shipping.processing_time)

            shipping.save()

        return instance

