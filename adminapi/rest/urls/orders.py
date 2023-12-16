from django.urls import path

from adminapi.rest.views.orders import AdminOrderList, AdminOrderDetail

urlpatterns = [
    path("", AdminOrderList.as_view(), name="admin-order-list"),
    path("<uuid:uid>", AdminOrderDetail.as_view(), name="admin-order-detail"),
]
