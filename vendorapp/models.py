from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.
from django.utils import timezone
choices = [
    ("CAN", "Canceled"),
    ("COMP", "Completed"),
    ("PEN", "Pending"),
]


class VendorManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        return user


class Vendor(AbstractBaseUser, PermissionsMixin):

    class Meta:
        db_table = "Vendor"
        verbose_name = "Vendor"

    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True, unique=True)
    contact_details = models.TextField(default='contact_details',null=True)
    address = models.TextField(default='address',null=True)
    vendor_code = models.CharField(unique=True, max_length=100)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rate = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'name'

    objects = VendorManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def __str__(self) -> str:
        return f"{self.name}"


class PurchaseOrder(models.Model):
    po_number = models.CharField(unique=True, max_length=200,null=True)
    vendor = models.ForeignKey(
        Vendor, related_name="purchaseorder", on_delete=models.CASCADE,null=True)
    order_date = models.DateTimeField(auto_now=True)
    delivery_date= models.DateTimeField(null=True)
    delivered_date= models.DateTimeField(null=True)
    items = models.JSONField(null=True,default=dict)
    quantity = models.IntegerField(default=0)
    status = models.CharField(choices=choices, max_length=50,default='pending')
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(null=True)
    acknowledgment_date = models.DateTimeField(null=True)


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(
        Vendor, related_name="history", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, auto_created=True)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)

    class Meta:
        db_table = "HistoricalPerformance"
