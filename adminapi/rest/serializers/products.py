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
    final_price = serializers.SerializerMethodField()
    avg_rating = serializers.CharField(source="averagereview", read_only=True)

    class Meta:
        model = Product
        fields = [
            "uid",
            "slug",
            "title",
            "price",
            "discount",
            "image",
            "status",
            "final_price",
            "avg_rating",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uid", "slug", "created_at", "updated_at"]

    def get_final_price(self, object_):
        return object_.price * (1 - (object_.discount / decimal.Decimal(100)))
