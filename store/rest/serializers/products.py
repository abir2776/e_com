import decimal

from rest_framework import serializers, generics

from versatileimagefield.serializers import VersatileImageFieldSerializer

from core.models import User

from store.models import Product, ReviewRating


class UserSlimSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="get_full_name", read_only=True)
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ]
    )

    class Meta:
        model = User
        fields = ["name", "email", "phone", "avatar"]
        read_only_fields = ("__all__",)


class ProductRatingSlimSerializer(serializers.ModelSerializer):
    user = UserSlimSerializer(read_only=True)

    class Meta:
        model = ReviewRating
        fields = [
            "uid",
            "user",
            "subject",
            "review",
            "rating",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uid", "user", "created_at", "updated_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        request = self.context["request"]
        uid = request.parser_context["kwargs"].get("uid")
        product = generics.get_object_or_404(
            Product.objects.filter(),
            uid=uid,
        )
        review = ReviewRating.objects.create(
            product=product, user=user, **validated_data
        )
        return review


class CustomerProductListSerializer(serializers.ModelSerializer):
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
            "image",
            "status",
            "quantity",
            "final_price",
            "avg_rating",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("__all__",)


class CustomerProductDetailSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ]
    )
    final_price = serializers.CharField(source="get_final_price", read_only=True)
    avg_rating = serializers.CharField(source="averagereview", read_only=True)
    ratings = ProductRatingSlimSerializer(
        source="reviewrating_set", read_only=True, many=True
    )

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
            "quantity",
            "final_price",
            "avg_rating",
            "ratings",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("__all__",)
