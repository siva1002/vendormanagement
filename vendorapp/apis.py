from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView, CreateAPIView
from .models import PurchaseOrder, Vendor
from .serializer import (PurchaseSerializer, VendorSerializer, VendorCreationSerializer,
                         VendorUpdateSerializer, VendorPerfomanceSerializer, LoginSerializer)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q, F, Count, Avg, ExpressionWrapper,FloatField,Sum,Func
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from functools import reduce
from datetime import timedelta

class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = authenticate(
                username=data["username"], password=data["password"])
            if not user:
                return Response({'error': 'Invalid Credentials'},
                                status=status.HTTP_403_FORBIDDEN)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key},
                            status=status.HTTP_200_OK)


class PurchaseAPI(ListCreateAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            deliverys = PurchaseOrder.objects.all()
            serialized = PurchaseSerializer(deliverys, many=True)
            return Response({"status": status.HTTP_200_OK, "data": serialized.data})
        except Exception as e:
            return Response({"status": status.HTTP_204_NO_CONTENT, "data": e})

    def post(self, request,):
        serializer = PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": status.HTTP_201_CREATED, "data": serializer.data})
        return Response({"status": status.HTTP_205_RESET_CONTENT, "error": serializer.errors})


class PurchaseUpdateAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [AllowAny]
    queryset = PurchaseOrder.objects.all()

    def put(self, request, *args, **kwargs):
        po = self.get_object()
        serializer = PurchaseSerializer(po, data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({"errors": serializer.errors}, status=status.HTTP_206_PARTIAL_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=200)


class VendorsGetUpdateAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = VendorUpdateSerializer
    permission_classes = [AllowAny]
    queryset = Vendor.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            vendors = Vendor.objects.get(id=kwargs['pk'])
            serialized = VendorSerializer(vendors)
            return Response({"data": serialized.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"data": str(e)}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, **kwargs):
        vendor = self.get_object()
        serializer = VendorUpdateSerializer(vendor, data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({"errors": serializer.errors}, status=status.HTTP_206_PARTIAL_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=200)


class VendorsCreate(ListCreateAPIView):
    serializer_class = VendorCreationSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            vendors = Vendor.objects.all()
            serialized = VendorSerializer(vendors, many=True)
            return Response({"data": serialized.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"data": e}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = VendorCreationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_206_PARTIAL_CONTENT)


class VendorPerformance(ListAPIView):
    serializer_class = VendorPerfomanceSerializer
    permission_classes = [AllowAny]
    queryset = Vendor.objects.all()
    def add(self,a, b): 
        return a + (b[0]-b[1])  
    def get(self, request, *args, **kwargs):
        # Get vendor details along with overall completed po and average of quality rating
        vendor = Vendor.objects.prefetch_related('purchaseorder').annotate(
            deliveryrate=Count('purchaseorder', filter=Q(purchaseorder__status__icontains='COM',
                               purchaseorder__delivery_date__lte=F("purchaseorder__delivery_date"))),
            quality_rating_avg=Avg('purchaseorder__quality_rating'),
            fullfilment_rate=ExpressionWrapper(Count('purchaseorder', filter=Q(purchaseorder__status__icontains='COM'))*1.0/Count('purchaseorder'),output_field=FloatField()),
            ).get(pk=kwargs['pk'])
        # li=vendor.purchaseorder.values_list("acknowledgment_date",'issue_date')
        # avgresponsetime=reduce(self.add,li,timedelta(0))/len(li)
        # vendor.__setattr__("average_response_time",avgresponsetime)           
        

        serialized = VendorPerfomanceSerializer(vendor)
        return Response({"data": serialized.data}, status=status.HTTP_200_OK)
