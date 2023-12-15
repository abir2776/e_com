from django.urls import path, include

urlpatterns = [path("products/", include("adminapi.rest.urls.products"))]
