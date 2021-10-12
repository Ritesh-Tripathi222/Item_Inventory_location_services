from rest_framework import serializers
from .models import Inventory
import logging

logger = logging.getLogger('iilservice')


class InventorySerializer(serializers.Serializer):
    """ Inventory Serializer Class Attributes"""
    id = serializers.IntegerField(read_only=True)
    sku = serializers.CharField(source='item')
    ref_location_id = serializers.CharField(source='location')
    quantity_unit = serializers.CharField(max_length=50, required=False)
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2,
                                        required=False)
    lot_no = serializers.CharField(max_length=100, required=False)
    expiry_date = serializers.CharField(max_length=100, required=False)
    flag_sth = serializers.CharField(max_length=100, required=False)
    flag_bopis = serializers.CharField(max_length=100, required=False)

    """ Meta Information """
    class Meta:
        model = Inventory
        fields = '__all__'



class InventoryDetailSerializer(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(read_only=True, source='item')
    sku = serializers.SlugRelatedField(read_only=True, slug_field='sku', source='item')
    item_name=serializers.SlugRelatedField(read_only=True, slug_field='name', source='item')
    location_id = serializers.PrimaryKeyRelatedField(read_only=True,source='location')
    ref_location_id = serializers.SlugRelatedField(read_only=True, slug_field='ref_location_id', source='location')
    location_name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='location')
    inventory_id = serializers.IntegerField(read_only=True, source='id')
    lot_no = serializers.CharField(max_length=100, required=False)
    expiry_date = serializers.CharField(max_length=100, required=False)
    flag_sth = serializers.CharField(max_length=100, required=False)
    flag_bopis = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = Inventory
        exclude = ['id', 'status_code', 'date_created', 'date_updated', 'updated_by_id', 'updated_by_role', 'item', 'location']


class InventoryListSerializer(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(read_only=True, source='item')
    sku = serializers.SlugRelatedField(read_only=True, slug_field='sku', source='item')
    location_id = serializers.PrimaryKeyRelatedField(read_only=True,source='location')
    ref_location_id = serializers.SlugRelatedField(read_only=True, slug_field='ref_location_id', source='location')
    inventory_id = serializers.IntegerField(read_only=True, source='id')
    lot_no = serializers.CharField(max_length=100, required=False)
    expiry_date = serializers.CharField(max_length=100, required=False)
    flag_sth = serializers.CharField(max_length=100, required=False)
    flag_bopis = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = Inventory
        exclude = ['status_code', 'date_created', 'date_updated', 'updated_by_id', 'updated_by_role', 'item', 'location']
