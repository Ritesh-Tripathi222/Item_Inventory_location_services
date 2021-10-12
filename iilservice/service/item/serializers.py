from rest_framework import serializers
from .models import Item, ItemDetail, ItemSellingInfo, ItemPurchaseInfo
import random
from datetime import datetime
from django.conf import settings

ITEM_COL = [f.name for f in Item._meta.get_fields() if f.name not in ['itemdetail', 'inventory','itempurchaseinfo', 'itemsellinginfo', 'client_id', 'date_created', 'date_updated', 'updated_by_id', 'updated_by_role']]
ITEM_DETAIL_COL = [f.name for f in ItemDetail._meta.get_fields() if f.name not in ['item', 'date_created', 'date_updated', 'updated_by_id', 'updated_by_role']]
ITEM_PURCHASE_COL = [f.name for f in ItemPurchaseInfo._meta.get_fields() if f.name not in ['item', 'date_created', 'date_updated', 'updated_by_id', 'updated_by_role']]
ITEM_SELL_COL = [f.name for f in ItemSellingInfo._meta.get_fields() if f.name not in ['item', 'date_created', 'date_updated', 'updated_by_id', 'updated_by_role']]
TODAY_DATE = datetime.today()



class ItemListSerializer(serializers.ModelSerializer):
    """ Item List View serializer """
    status = serializers.CharField()

    class Meta:
        model = Item
        exclude = ("date_created",'date_updated','updated_by_role','updated_by_id','status_code')

class ItemDetailSerializer(serializers.ModelSerializer):
    """ Item  View serializer """
    status = serializers.CharField()

    class Meta:
        model = Item
        exclude = ("date_created",'date_updated','updated_by_role','updated_by_id','status_code')


class DetailInfoSerializer(serializers.ModelSerializer):
    """ full add update work """
    description = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)
    dimension_unit = serializers.CharField(required=False)
    dimension_x = serializers.DecimalField(required=False, max_digits=5, decimal_places=2, default=0.00)
    dimension_y = serializers.DecimalField(required=False, max_digits=5, decimal_places=2, default=0.00)
    dimension_z = serializers.DecimalField(required=False, max_digits=5, decimal_places=2, default=0.00)
    weight_unit = serializers.CharField(required=False)
    weight = serializers.DecimalField(required=False, max_digits=5, decimal_places=2, default=0.00)
    lead_time = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, default=0.00)
    lead_time_unit = serializers.CharField(required=False)
    protection_level = serializers.CharField(required=False)
    min_quantity = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, default=0.00)
    channel_type = serializers.CharField(required=False)
    is_dropship_only = serializers.CharField(required=False, default='yes')
    shipping_restrictions = serializers.CharField(required=False)
    delivery_method = serializers.CharField(required=False)
    fulfillment_types = serializers.CharField(required=False)
    shipping_service_level = serializers.CharField(required=False)
    is_returnable = serializers.CharField(required=False)
    manufacturer = serializers.CharField(required=False)
    vendor_name = serializers.CharField(required=False)
    mpn = serializers.CharField(required=False)
    isbn = serializers.CharField(required=False)

    class Meta:
        model = ItemDetail
        fields = ITEM_DETAIL_COL


class SellingInfoSerializer(serializers.ModelSerializer):
    selling_price_unit = serializers.CharField(required=False)
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0.00)
    selling_account = serializers.CharField(required=False)
    selling_account_id = serializers.CharField(required=False)
    sales_description = serializers.CharField(required=False)
    sales_tax = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, default=0.00)

    class Meta:
        model = ItemSellingInfo
        fields = ITEM_SELL_COL


class PurchaseInfoSerializer(serializers.ModelSerializer):
    purchase_price_unit = serializers.CharField(required=False)
    purchase_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False,default=0.00)
    purchase_account = serializers.CharField(required=False)
    purchase_account_id = serializers.CharField(required=False)
    purchase_description = serializers.CharField(required=False)
    purchase_tax = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, default=0.00)

    class Meta:
        model = ItemPurchaseInfo
        fields = ITEM_PURCHASE_COL


class ItemSerializer(serializers.ModelSerializer):
    """ nested serializers """
    id = serializers.IntegerField(read_only=True)
    status = serializers.ChoiceField(choices=settings.STATUS_CHOICES_LIST, source='status_code', required=False)
    status_code = serializers.ChoiceField(choices=settings.STATUS_CHOICES_LIST, required=False)
    upc = serializers.CharField(max_length=50, required=False)
    ean = serializers.CharField(max_length=50, required=False)
    size = serializers.CharField(max_length=50, required=False)
    barcode = serializers.CharField(max_length=50, required=False)
    department = serializers.CharField(max_length=50, required=False)
    item_class = serializers.CharField(max_length=50, required=False)
    unit = serializers.CharField(max_length=50, required=False)
    short_description = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)
    description = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)
    dimension_unit = serializers.CharField(required=False)
    dimension_x = serializers.DecimalField(required=False, max_digits=5, decimal_places=2, default=0.00)
    dimension_y = serializers.DecimalField(required=False, max_digits=5, decimal_places=2, default=0.00)
    dimension_z = serializers.DecimalField(required=False, max_digits=5, decimal_places=2, default=0.00)
    weight_unit = serializers.CharField(required=False)
    weight = serializers.DecimalField(required=False, max_digits=5, decimal_places=2, default=0.00)
    lead_time = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, default=0.00)
    lead_time_unit = serializers.CharField(required=False)
    protection_level = serializers.CharField(required=False)
    min_quantity = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, default=0.00)
    channel_type = serializers.CharField(required=False)
    is_dropship_only = serializers.CharField(required=False, default='yes')
    shipping_restrictions = serializers.CharField(required=False)
    delivery_method = serializers.CharField(required=False)
    fulfillment_types = serializers.CharField(required=False)
    shipping_service_level = serializers.CharField(required=False)
    is_returnable = serializers.CharField(required=False)
    manufacturer = serializers.CharField(required=False)
    vendor_name = serializers.CharField(required=False)
    mpn = serializers.CharField(required=False)
    isbn = serializers.CharField(required=False)
    selling_info=SellingInfoSerializer(write_only=True,required=False,many=True) # sellingInfoSerializer
    purchase_info = PurchaseInfoSerializer(write_only=True,required=False,many=True) # purchase info serializer

    class Meta:
        model = Item
        fields = ITEM_COL + ['status']+ITEM_DETAIL_COL+['purchase_info','selling_info']

    def create(self, validated_data):
        item_data = dict()
        detail_data = dict()
        purchase_data = dict()
        sell_data = dict()
        item_data['client_id'] = random.randint(1, 100000000)

        item_data['date_created'] = TODAY_DATE
        detail_data['date_created'] = TODAY_DATE
        purchase_data['date_created'] = TODAY_DATE
        sell_data['date_created'] = TODAY_DATE
        for k in validated_data:
            if k in ITEM_COL:
                item_data[k] = validated_data[k]

            if k in ITEM_DETAIL_COL:
                detail_data[k] = validated_data[k]
        if 'status_code' in validated_data:
            st = (v[0] for v in settings.STATUS_CHOICES if v[1] == validated_data['status_code'])
            item_data['status_code'] = next(st)

        item_obj = Item.objects.create(**item_data)

        detail_data['item'] = item_obj
        purchase_data['item'] = item_obj
        sell_data['item'] = item_obj

        ItemDetail.objects.create(**detail_data)

        if 'purchase_info' in validated_data:
            purchase_info = validated_data.pop('purchase_info')
            for purchase_data in purchase_info:
                ItemPurchaseInfo.objects.create(**purchase_data,item=item_obj)

        if 'selling_info' in validated_data:
                selling_info = validated_data.pop('selling_info')
                for sell_data in selling_info:
                    ItemSellingInfo.objects.create(**sell_data,item=item_obj)
        return item_obj


class DetailFields(serializers.ModelSerializer):
    """ detail serializer for imcluding in search serializer"""
    #id = serializers.IntegerField(required=False)

    class Meta:
        model = ItemDetail
        fields=['delivery_method','manufacturer','vendor_name']


class GenericUpdateSerializer(serializers.Serializer):
    class Meta:
        model = Item


class ItemSearchSerializer(serializers.ModelSerializer):
    """ search serializer """
    #manufacturer = serializers.SlugRelatedField(required=False, slug_field='manufacturer', source='itemdetail',read_only=True)
    itemdetail=DetailFields(many=True,read_only=True)
    status = serializers.CharField()
    class Meta:
        model = Item
        exclude = ('date_created','date_updated','updated_by_role','updated_by_id','status_code')
