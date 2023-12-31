from django.urls import path

from store.rest.views import products

urlpatterns = [
    path(
        "<uuid:uid>/ratings",
        products.CustomerProductRatingListView.as_view(),
        name="customer-product-rating-list",
    ),
    path(
        "<uuid:uid>",
        products.CustomerProductDetailView.as_view(),
        name="customer-product-detail",
    ),
    path("", products.CustomerProductListView.as_view(), name="customer-products-list"),
]
