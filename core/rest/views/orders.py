from rest_framework import generics

from core.rest.serializers.orders import MeOrderSerializer

from order.models import Order


class MeOrderList(generics.ListCreateAPIView):
    serializer_class = MeOrderSerializer

    def get_queryset(self):
        return Order.objects.prefetch_related("orderitems_set").filter(
            user=self.request.user
        )
