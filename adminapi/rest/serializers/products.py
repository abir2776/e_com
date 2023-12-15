import decimal

from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from store.models import Product


class AdminProductSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ]
    )
    final_price = serializers.CharField(source="get_final_price", read_only=True)
    avg_rating = serializers.CharField(source="averagereview", read_only=True)

    class Meta:
        model = Product
        fields = [
            "uid",
            "slug",
            "title",
            "price",
            "discount",
            "quantity",
            "image",
            "status",
            "final_price",
            "avg_rating",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uid", "slug", "created_at", "updated_at"]
