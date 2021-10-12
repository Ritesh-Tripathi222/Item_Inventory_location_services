from rest_framework.generics import ListAPIView
from django.http import HttpResponse, JsonResponse
from .serializers import InventorySerializer, InventoryListSerializer,InventoryDetailSerializer
from .models import Inventory, InventoryAttributeSettings, InventoryAttributeInfo
from item.models import Item
from location.models import Location
import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
from django_filters import rest_framework as filters
# Create your views here.
logger = logging.getLogger('iilservice')
INVENTORY_ATTR = ['lot_no', 'expiry_date', 'flag_sth', 'flag_bopis']


class InventoryAddView(generics.CreateAPIView):
    serializer_class = InventorySerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            sku = data['sku']
            loc_id = data['ref_location_id']
            item = Item.objects.filter(sku=sku).get()
            location = Location.objects.filter(ref_location_id=loc_id).get()
            inventory_data = dict()
            inventory_data['quantity'] = data['quantity']
            inventory_data['quantity_unit'] = data['quantity_unit']

            inventory_object = Inventory.objects.create(**inventory_data, item=item, location=location)
            get_attr = [attr for attr in INVENTORY_ATTR if attr in data]
            for obj in InventoryAttributeSettings.objects.filter(name__in=get_attr):
                InventoryAttributeInfo.objects.create(
                    inventory=inventory_object,
                    inventory_attribute=obj,
                    inventory_attribute_value=data[obj.name])
            success_msg = {
                    "success": "true",
                    "code": 0,
                    "message": "The inventory details has been added.",
                    "item_id": item.id,
                    "location_id": location.id,
                    "inventory_id": inventory_object.id
                }
            return JsonResponse(success_msg, safe=False, status=status.HTTP_200_OK)

        except Item.DoesNotExist:
            msg = {
                "success": "fail",
                "code": 0,
                "message": "The inventory details has not been added.",
                'sku': "The given Sku does not exist"
            }
            return JsonResponse(msg, status=412)
        except Location.DoesNotExist:
            msg = {
                "success": "fail",
                "code": 0,
                "message": "The inventory details has not been added.",
                "ref_location_id": "The given ref_location_id does not exist"
            }
            return JsonResponse(msg, status=412)
        except Exception:
            msg = {
                "success": "fail",
                "code": 0,
                "message": "The inventory details has not been added.",
                "info": "Internal Server error"
            }
            return JsonResponse(msg, safe=False, status=500)


class InventoryListPagination(LimitOffsetPagination):
    default_limit = 20
    page_size_query_param = 'page'
    max_limit = 1000

    def get_paginated_response(self, data):
        return Response(data)


class InventoryListView(ListAPIView):
    """ Inventory List View """
    serializer_class = InventoryListSerializer
    pagination_class = InventoryListPagination

    def get_queryset(self):
        try:
            queryset = Inventory.objects.all()
            for key in queryset:
                if key.inventoryattributeinfo_set.count():
                    for idx in key.inventoryattributeinfo_set.filter(inventory=key):
                        key.__dict__[idx.inventory_attribute.name] = idx.inventory_attribute_value
            return queryset
        except Exception:
            return Inventory.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            custom_response = {
                'sucess': 'true',
                'code': 0,
                'message': "success",
                "inventory": response.data
            }
            return Response(custom_response, status=status.HTTP_200_OK)
        except Exception as msg:
            return Response({
                "success": "false",
                "code": 500,
                "message": "Internal Server Error",
            }, status=500)


class ItemFilter(FilterSet):
    """ Custom Search Filter Set """
    inventory_id=filters.CharFilter('id')
    item_id = filters.CharFilter('item_id')
    location_id = filters.CharFilter('location_id')
    ref_location_id = filters.CharFilter('location__ref_location_id')
    sku= filters.CharFilter('item__sku')

    class Meta:
        model = Inventory
        fields = ('inventory_id','item_id', 'location_id', 'ref_location_id','sku')

class InventrySearch(generics.ListAPIView):
    """ inventry search """
    queryset = Inventory.objects.all()
    serializer_class = InventoryListSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = ItemFilter


class InventoryDetailview(generics.RetrieveAPIView):
    """ Inventory Detail View"""
    serializer_class = InventoryDetailSerializer

    @property
    def data(self):
        return self.serializer_class(self.get_queryset()[0]).data

    def get_queryset(self):
        try:
            queryset = Inventory.objects.filter(pk=self.kwargs['pk'])
            for key in queryset:
                if key.inventoryattributeinfo_set.count():
                    for idx in key.inventoryattributeinfo_set.filter(inventory=key):
                        key.__dict__[idx.inventory_attribute.name] = idx.inventory_attribute_value
            return queryset
        except Exception:
            return queryset.objects.none()

    def get(self, request, *args, **kwargs):
        try:
            data = self.data
            data['success'] = "true"
            data['code'] = 0
            data['message'] = "success"
            return JsonResponse(data, status=200)
        except Exception:
            res = {
                "success": "fail",
                "code": 0,
                "message": "Object Does not exist"
            }
            return JsonResponse(res, status=500)




