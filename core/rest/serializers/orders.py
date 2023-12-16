from django.core.validators import MinValueValidator

from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from order.models import Order, OrderItems

from store.models import Product


class MeOrderItemsSerializer(serializers.ModelSerializer):
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


class MeOrderSerializer(serializers.ModelSerializer):
    products = MeOrderItemsSerializer(
        source="orderitems_set", many=True, read_only=True
    )
    product = serializers.SlugRelatedField(
        queryset=Product.objects.get_status_active(), slug_field="slug", write_only=True
    )
    quantity = serializers.IntegerField(
        validators=[MinValueValidator(1)], write_only=True
    )
    total_final_price = serializers.CharField(source="get_total_price", read_only=True)

    class Meta:
        model = Order
        fields = [
            "uid",
            "products",
            "product",
            "quantity",
            "total_final_price",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "uid",
            "products",
            "total_final_price",
            "status",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        product = validated_data.pop("product", None)
        quantity = validated_data.pop("quantity", None)
        if product.quantity < quantity:
            raise serializers.ValidationError("There is not enough product in stock!")
        product.quantity = product.quantity - quantity
        product.save()
        order = Order.objects.create(user=self.context["request"].user)
        OrderItems.objects.create(order=order, product=product, quantity=quantity)
        return order
