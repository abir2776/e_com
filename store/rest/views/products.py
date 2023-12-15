from rest_framework.generics import ListAPIView, RetrieveAPIView

from django.db.models import Prefetch

from store.rest.serializers import products

from store.models import Product, ReviewRating


class CustomerProductListView(ListAPIView):
    queryset = Product.objects.prefetch_related(
        Prefetch("reviewrating_set", queryset=ReviewRating.objects.filter(status=True))
    ).get_status_active()
    serializer_class = products.CustomerProductListSerializer


class CustomerProductDetailView(RetrieveAPIView):
    queryset = Product.objects.prefetch_related(
        Prefetch("reviewrating_set", queryset=ReviewRating.objects.filter(status=True))
    ).get_status_active()
    serializer_class = products.CustomerProductDetailSerializer
    lookup_field = "uid"
