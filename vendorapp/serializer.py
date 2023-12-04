from rest_framework import (serializers)
from .models import (PurchaseOrder,Vendor)

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model=PurchaseOrder
        fields='__all__'

class VendorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Vendor
        fields='__all__'
        extra_kwargs = {"address": {"required": False, "allow_null": True},
                        "contact_details": {"required": False, "allow_null": True},
                        "password":{"write_only":True}}

class VendorCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields=("email","name","password","contact_details","vendor_code","address")
        extra_kwargs = {"address": {"required": False, "allow_null": True},
                        "contact_details": {"required": False, "allow_null": True}}
    def create(self,validateddata):
        vendor=Vendor.objects.create_user(**validateddata)
        vendor.set_password(validateddata["password"])
        vendor.save()
        return vendor

class VendorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields=("email","name","contact_details","vendor_code","address")
        extra_kwargs = {"address": {"required": False, "allow_null": True},
                        "contact_details": {"required": False, "allow_null": True},
                        "vendor_code": {"required": False, "allow_null": True}}
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.contact_details = validated_data.get('contact_details ', instance.contact_details )
        instance.vendor_code=validated_data.get('vendor_code', instance.vendor_code)
        instance.address=validated_data.get('address', instance.address)
        return instance
    
class VendorPerfomanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields=("name","vendor_code","on_time_delivery_rate","quality_rate","average_response_time","fulfillment_rate")
    
