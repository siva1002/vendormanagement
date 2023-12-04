from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView, CreateAPIView
from .models import PurchaseOrder, Vendor
from .serializer import (PurchaseSerializer, VendorSerializer, VendorCreationSerializer,
                         VendorUpdateSerializer, VendorPerfomanceSerializer, LoginSerializer)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from django.utils import timezone
from datetime import datetime


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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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

class AcknowledgePurchaseOrder(ListAPIView):
    serializer_class=PurchaseSerializer
    permission_classes=[IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    def get(self, request, *args, **kwargs):
        pk=kwargs.pop('pk', None)
        if pk:
            po=get_object_or_404(PurchaseOrder, pk=pk)
            if not po.acknowledgment_date:
                timzone_datetime = timezone.make_aware(datetime.now())
                po.acknowledgment_date=timzone_datetime
                po.save()
                serializer=PurchaseSerializer(po)
            return Response({"message":"Purchase Order Acknowledged Already" }, status=status.HTTP_200_OK)
        
        



class VendorPerformance(ListAPIView):
    serializer_class = VendorPerfomanceSerializer
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    def get(self, request, *args, **kwargs):
        vendor=get_object_or_404(Vendor,pk=kwargs['pk'])  
        serialized = VendorPerfomanceSerializer(vendor)
        return Response({"data":serialized.data }, status=status.HTTP_200_OK)
