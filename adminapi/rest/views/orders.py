from rest_framework import generics

from adminapi.rest.serializers.orders import AdminOrderSerializer
from adminapi.permissions import IsStaff

from order.models import Order


class AdminOrderList(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("orderitems_set").filter()
    serializer_class = AdminOrderSerializer
    permission_classes = [IsStaff]


class AdminOrderDetail(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.filter()
    serializer_class = AdminOrderSerializer
    permission_classes = [IsStaff]
    lookup_field = "uid"
