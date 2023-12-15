from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView

from rest_framework import generics

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


class CustomerProductRatingListView(ListCreateAPIView):
    serializer_class = products.ProductRatingSlimSerializer

    def get_queryset(self):
        uid = self.kwargs.get("uid", None)
        product = generics.get_object_or_404(Product.objects.filter(), uid=uid)
        return ReviewRating.objects.filter(product=product, status=True)
