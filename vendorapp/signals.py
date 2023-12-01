from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from .models import Vendor
from django.db.models import Q, F, Count, Avg, ExpressionWrapper,FloatField,Sum,Func



@receiver(post_save, sender=PurchaseOrder)
def my_handler(sender,instance, **kwargs):
    performance = PurchaseOrder.objects.prefetch_related('vendor').filter(vendor=instance.vendor).annotate(
            deliveryrate=Count(Q(status__icontains='COM',delivery_date__lte=F("delivery_date"))),
            quality_rating_avg=Avg('quality_rating'),
            fullfilment_rate=ExpressionWrapper(Count(Q(status__icontains='COM'))*1.0/Count('id'),output_field=FloatField()),
            completed=Count(Q(status__iexact='COM'),default=0),
            count=Count('id')
            )
    # performance=PurchaseOrder.objects.filter(vendor=instance.vendor,status__iexact="COM")
    # print(performance.count())
    for i in performance:
        print(i.__dict__)
    