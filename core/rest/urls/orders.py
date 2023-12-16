from django.urls import path

from core.rest.views.orders import MeOrderList, MeOrderDetail

urlpatterns = [
    path("", MeOrderList.as_view(), name="order-list"),
    path("<uuid:uid>", MeOrderDetail.as_view(), name="order-detail"),
]
