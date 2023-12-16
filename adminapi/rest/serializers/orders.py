from django.core.validators import MinValueValidator

from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from order.models import Order, OrderItems

from store.models import Product


class AdminOrderItemsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="product.title", read_only=True)
    slug = serializers.CharField(source="product.slug", read_only=True)
    price = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2, source="product.price"
    )
    discount = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2, source="product.discount"
    )
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        read_only=True,
        source="product.image",
    )
    total_price = serializers.CharField(source="get_total", read_only=True)

    class Meta:
        model = OrderItems
        fields = [
            "slug",
            "title",
            "price",
            "discount",
            "image",
            "quantity",
            "total_price",
        ]
        read_only_fields = ("__all__",)


class AdminOrderSerializer(serializers.ModelSerializer):
    products = AdminOrderItemsSerializer(
        source="orderitems_set", many=True, read_only=True
    )
    total_final_price = serializers.CharField(source="get_total_price", read_only=True)

    class Meta:
        model = Order
        fields = [
            "uid",
            "products",
            "total_final_price",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "uid",
            "products",
            "total_final_price",
            "created_at",
            "updated_at",
        ]
