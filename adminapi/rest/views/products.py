from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from adminapi.permissions import IsStaff
from django.db.models import Prefetch

from adminapi.rest.serializers import products

from store.models import Product, ReviewRating


class AdminProductListView(ListCreateAPIView):
    queryset = Product.objects.prefetch_related(
        Prefetch("reviewrating_set", queryset=ReviewRating.objects.filter(status=True))
    ).get_status_editable()
    serializer_class = products.AdminProductSerializer
    permission_classes = [IsStaff]


class AdminProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.prefetch_related(
        Prefetch("reviewrating_set", queryset=ReviewRating.objects.filter(status=True))
    ).get_status_editable()
    serializer_class = products.AdminProductSerializer
    permission_classes = [IsStaff]
    lookup_field = "uid"
