from django.urls import path

from adminapi.rest.views import products

urlpatterns = [
    path(
        "<uuid:uid>",
        products.AdminProductDetailView.as_view(),
        name="admin-product-detail",
    ),
    path("", products.AdminProductListView.as_view(), name="admin-products-list"),
]
