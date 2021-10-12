from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from location.models import *
from location.serializers import *
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet


class LocationList(generics.ListAPIView):
    """ For List View """
    def get(self,request,format='json'):
        location = Location.objects.values("id","name", "ref_location_id","location_type_id","timezone","currency","payment_terms","address1","address2","city","state","postal_code","country_code")
        main = {'success':"true","code":0,"message":"success",'locations':location}
        return Response(main)

class LocationSearch(generics.ListAPIView):
    """ For Search """
    queryset = Location.objects.all()
    serializer_class = LocationSearchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name','ref_location_id','address1','address2','city','state','postal_code']

class LocationAdd(generics.CreateAPIView):
    """ For Add View """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return JsonResponse({
            "success": "true",
            "code": 0,
            "message": "The location has been added.",
            "location_id": response.data['id']
            }, safe=False, status=status.HTTP_200_OK)


class LocationDetail(APIView):
    """ For Detail View """
    def get(self, request,pk=None,format=None):

        location_pk = get_object_or_404(Location, pk=pk)

        location = Location.objects.filter(id=location_pk.id).values("id","name", "ref_location_id","location_type_id","timezone","currency","payment_terms","address1","address2","city","state","postal_code","country_code")
        location_contact = LocationContactInfo.objects.filter(location_id=location_pk.id).values('first_name','last_name','designation','phone','email')
        receiving = LocationReceivingInfo.objects.filter(location_id=location_pk.id).values('day','receiving_start_time','receiving_end_time','service_level_id','carrier_last_pickup','receiving_capacity','processing_time_unit','processing_time','additional_info')
        shipping = LocationShippingInfo.objects.filter(location_id=location_pk.id).values('day','shipping_start_time','shipping_end_time','service_level_id','carrier_last_pickup','shipping_capacity','processing_time_unit','processing_time','additional_info')

        main = {
        'success':"true",
        "code":0,
        "message":"success",
        'location':location,
        'contact_info':location_contact,
        'receiving_info':receiving,
        'shipping_info':shipping}

        return Response(main)



class LocationEdit(generics.UpdateAPIView):
    serializer_class = LocationSearchSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        try:
            return Location.objects.get(id=self.kwargs['pk'])
        except ObjectDoesNotExist as e:
            return None

    def put(self, request, *args, **kwargs):
        location_id = kwargs['pk']
        location = Location.objects.filter(pk=location_id)
        if location:
            data = request.data
            location_update = dict()
            contact_update = dict()
            receiving_update = dict()
            shipping_update = dict()
            for k in data:
                if k in LOCATION_COL:
                    if k != 'ref_location_id':
                        location_update[k] = data[k]

            if location.update(**location_update):
                if 'contact_info' in data:
                    contact_info = data.pop('contact_info')
                    for k in contact_info:
                        if k in CONTACT_INFO:
                            contact_update[k] = contact_info[k]
                    LocationContactInfo.objects.filter(location_id=location_id).update(**contact_update)

                if 'receiving_info' in data:
                    receiving_info = data.pop('receiving_info')
                    for k in receiving_info:
                        if k in RECEIVING_INFO:
                            receiving_update[k] = receiving_info[k]
                    LocationReceivingInfo.objects.filter(location_id=location_id).update(**receiving_update)

                if 'shipping_info' in data:
                    shipping_info = data.pop('shipping_info')
                    for k in shipping_info:
                        if k in SHIPPING_INFO:
                            shipping_update[k] = shipping_info[k]
                    LocationShippingInfo.objects.filter(location_id=location_id).update(**shipping_update)

                res = {
                    "success": "true",
                    "code": 0,
                    "message": "The location has been updated.",
                    "location_id": location_id
                }
                return JsonResponse(res, status=status.HTTP_200_OK)
            else:
                res = {
                    "success": "fail",
                    "code": 0,
                    "message": "The location has not been updated.",
                    "location_id": location_id
                }
                return JsonResponse(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse({'msg': 'Objects does not exist'}, safe=False, status=status.HTTP_412_PRECONDITION_FAILED)
