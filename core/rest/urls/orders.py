from django.urls import path

from core.rest.views.orders import MeOrderList

urlpatterns = [path("", MeOrderList.as_view(), name="order-list")]
