from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import PurchaseOrder,Vendor,HistoricalPerformance
from django.db.models import Q, F, Count, Avg, ExpressionWrapper,FloatField,Sum,Func
from django import db



@receiver(post_save, sender=PurchaseOrder)
def performancehandler(sender,instance, **kwargs):
    vendor=instance.vendor
    vendor_po = PurchaseOrder.objects.prefetch_related('vendor').filter(vendor=vendor).annotate(diff=F("acknowledgment_date")-F("issue_date"))
    
    on_time_delivery_rate=vendor_po.filter(status__icontains="COMP",delivery_date__lte=F("delivery_date")).count()/vendor_po.count()
    rating_and_responsetime=vendor_po.aggregate(avg_response_time=Avg("diff"),quality_rating_avg=Avg('quality_rating',filter=Q(status__iexact="COMP")))
    fullfilmentrate=vendor_po.filter(status__icontains="COMP").count()/vendor_po.count()*100
    hp=HistoricalPerformance(vendor=vendor,on_time_delivery_rate=vendor.on_time_delivery_rate,quality_rating_avg=vendor.quality_rate,average_response_time=vendor.average_response_time,fulfillment_rate=vendor.fulfillment_rate)
   
    print(rating_and_responsetime,on_time_delivery_rate)
   
    vendor.average_response_time=rating_and_responsetime['avg_response_time'].total_seconds()  if rating_and_responsetime['avg_response_time'] else 0
    vendor.fulfillment_rate=fullfilmentrate
    vendor.quality_rate=rating_and_responsetime['quality_rating_avg'] if rating_and_responsetime['quality_rating_avg'] else 0
    vendor.on_time_delivery_rate=on_time_delivery_rate
    hp.save()
    vendor.save()

   