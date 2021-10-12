from rest_framework import generics
from .models import Item, ItemDetail, ItemPurchaseInfo, ItemSellingInfo
from item.serializers import ItemSerializer, ItemListSerializer, DetailInfoSerializer,ItemSearchSerializer, GenericUpdateSerializer, ITEM_COL, ITEM_DETAIL_COL, ITEM_PURCHASE_COL, ITEM_SELL_COL,ItemDetailSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django_filters import FilterSet
from django_filters import rest_framework as filters
from django.conf import settings


class ItemAdd(generics.CreateAPIView):
    """ Item Add with all info and details"""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return JsonResponse({
            "success": "true",
            "code": 0,
            "message": "The item has been added.",
            "item_id": response.data['id']
            }, safe=False, status=status.HTTP_200_OK)


class ItemList(generics.ListAPIView):
    serializer_class = ItemListSerializer

    @property
    def data(self):
        return self.serializer_class(self.get_queryset(),many=True).data

    def get_queryset(self):
        try:
            queryset = Item.objects.all()
            for key in queryset:
                key.status=key.get_status_code_display()  #get status as active inactive on call get
            return queryset
        except Exception:
            return Item.objects.none()

    def list(self, request, format=None,*args,**kwargs):
        try:
            super().list(request, *args, **kwargs)
            res = {'success':"true","code":0,"message":"success","item":self.data}
            return JsonResponse(res,status=200)
        except Exception:
            return JsonResponse({'success':"false","code":0,"message":"internal server error"},status=500)

class ItemFilter(FilterSet):
    """ Custom Search Filter Set """
    item_id=filters.CharFilter('id')
    name = filters.CharFilter('name')
    sku = filters.CharFilter('sku')
    item_class = filters.CharFilter('item_class')
    status_code= filters.CharFilter('status_code')
    delivery_method = filters.CharFilter('itemdetail__delivery_method')
    manufacturer = filters.CharFilter('itemdetail__manufacturer')
    vendor_name = filters.CharFilter('itemdetail__vendor_name')

    class Meta:
        model = Item
        fields = ('item_id','name', 'sku', 'item_class','status_code','manufacturer','delivery_method','vendor_name')


class ItemSearch(generics.ListAPIView):
    """ Item search """
    queryset = Item.objects.all()
    serializer_class = ItemSearchSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = ItemFilter
    #filterset_fields = ['status_code']

    @property
    def data(self):
        return self.serializer_class(self.filter_queryset(self.queryset),many=True).data

    def filter_queryset(self,queryset):
        sup=super().filter_queryset(self.queryset)
        try:
            queryset = sup
            for key in queryset:
                key.status=key.get_status_code_display()  #get status as active inactive on call get
            return queryset
        except Exception:
            return Item.objects.none()

    def list(self, request, format=None,*args,**kwargs):
        try:
            super().list(request, *args, **kwargs)
            res = {'success':"true","code":0,"message":"success","item":self.data}
            return JsonResponse(res,status=200)
        except Exception:
            return JsonResponse({'success':"false","code":0,"message":"internal server error"},status=500)


class ItemEditView(generics.UpdateAPIView):
    """ Item Edit and add when does not exists"""
    serializer_class = ItemSerializer
    lookup_field = 'item_id'

    def get_queryset(self):
        try:
            return Item.objects.get(id=self.kwargs['item_id'])
        except ObjectDoesNotExist as e:
            return Item.objects.none()

    def put(self, request, *args, **kwargs):
        try:
            item_id = kwargs['item_id']
            item = Item.objects.filter(id=item_id)
            if item:
                data = request.data
                item_update = dict()
                detail_update = dict()
                for k in data:                  #update item columns
                    if k in ITEM_COL:
                        item_update[k] = data[k]

                    if k in ITEM_DETAIL_COL:     #update detail columns
                        detail_update[k] = data[k]
                ItemDetail.objects.filter(item_id=item_id).update(**detail_update)
            
                if 'status' in data:
                    st = (v[0] for v in settings.STATUS_CHOICES if
                          v[1] == data['status'])
                    item_update['status_code'] = next(st)

                item.update(**item_update)
                ItemDetail.objects.filter(item_id=item_id).update(**detail_update)

                if 'purchase_info' in data:
                        purchase_info = data.pop('purchase_info')
                        for purchase_update in purchase_info:# enter k in nested purchase
                            ItemPurchaseInfo.objects.update_or_create(item_id=item_id, defaults=purchase_update) #if exists update else create

                if 'selling_info' in data:
                        selling_info = data.pop('selling_info')
                        for sell_update in selling_info:
                            ItemSellingInfo.objects.update_or_create(item_id=item_id, defaults=sell_update)

                res = {
                    "success": "true",
                    "code": 0,
                    "message": "The item has been updated.",
                    "item_id": item_id
                }
                return JsonResponse(res, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'msg': 'Item does not exist'}, safe=False, status=status.HTTP_412_PRECONDITION_FAILED)
        except StopIteration:
            return JsonResponse({'msg': 'Invalid value of status passed'}, status=500)
        except IntegrityError as msg:
            return JsonResponse({'msg': msg.args[1]}, status=500)
        except Exception:
            return JsonResponse({'msg': 'Internal Server Error'}, status=500)



class ItemDetailView(generics.RetrieveAPIView):
    """ For Detail View """
    serializer_class = ItemDetailSerializer

    @property
    def data(self):
        return self.serializer_class(self.get_queryset()[0]).data

    def get_queryset(self):
        try:
            queryset = Item.objects.filter(pk=self.kwargs['pk'])
            for key in queryset:
                key.status=key.get_status_code_display()
            return queryset
        except Exception:
            return queryset.objects.none()

    def get(self, request, pk=None, format=None):
        try:
            item_pk = get_object_or_404(Item, pk=pk)
            item_details = ItemDetail.objects.filter(item=item_pk.id).values('description','dimension_unit','dimension_x',
                                                                            'dimension_y','dimension_z','weight_unit',
                                                                            'weight','lead_time','lead_time_unit',
                                                                            'protection_level','min_quantity',
                                                                            'channel_type','is_dropship_only',
                                                                            'shipping_restrictions',
                                                                            'delivery_method','fulfillment_types',
                                                                            'shipping_service_level','is_returnable',
                                                                            'manufacturer','vendor_name','mpn','isbn')

            purchase_info = ItemPurchaseInfo.objects.filter(item=item_pk.id).values('purchase_price_unit','purchase_price',
                                                                                'purchase_account','purchase_account_id',
                                                                                'purchase_description','purchase_tax')

            selling_info = ItemSellingInfo.objects.filter(item=item_pk.id).values('selling_price_unit','selling_price',
                                                                                'selling_account','selling_account_id',
                                                                                'sales_description','sales_tax')
            item = self.data
            if len(item_details):
                item.update(item_details[0]) #updated item_detail to item from  nested to single dimension

            res = {
            'success': "true",
            "code": 0,
            "message": "success",
            'item': item,
            'purchase_info':purchase_info,
            'selling_info':selling_info,

        }
            return Response(res,status=200)
        except Exception:
            return Response({'success':"false","code":0,"message":"internal server error"},status=500)



