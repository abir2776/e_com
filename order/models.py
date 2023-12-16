import decimal

from django.conf import settings
from django.db import models
from django.db.models import F, DecimalField, ExpressionWrapper, Sum

from django.dispatch import receiver
from django.db.models.signals import pre_save

from common.models import BaseModelWithUID

from store.models import Product

from .choices import OrderDeliveryStatus


class Order(BaseModelWithUID):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_id = models.PositiveIntegerField(unique=True)
    status = models.CharField(
        max_length=50,
        default=OrderDeliveryStatus.ORDER_PLACED,
        choices=OrderDeliveryStatus.choices,
    )

    def get_total_price(self):
        total_price = self.orderitems_set.aggregate(
            total_price=Sum(
                ExpressionWrapper(
                    F("product__price") * (1 - F("product__discount") / 100),
                    output_field=DecimalField(),
                )
            )
        )["total_price"]
        return total_price


class OrderItems(BaseModelWithUID):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total(self):
        return self.product.get_final_price() * self.quantity

    def __str__(self):
        return f"{self.quantity} X {self.product}"


def generate_order_id():
    last_order = Order.objects.all().order_by("order_id").last()
    if not last_order:
        return 1
    return last_order.order_id + 1


@receiver(pre_save, sender=Order)
def set_order_id(sender, instance, **kwargs):
    if not instance.order_id:
        instance.order_id = generate_order_id()
