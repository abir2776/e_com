from django.db import models
from django.db.models import Avg

from autoslug import AutoSlugField

from versatileimagefield.fields import VersatileImageField

from common.models import BaseModelWithUID

from store.choices import ProductStatus

from .managers import ProductQuerySet


class Product(BaseModelWithUID):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="title")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = VersatileImageField(upload_to="product_image/", blank=True)
    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        db_index=True,
        default=ProductStatus.PUBLISHED,
    )
    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return self.title

    def averagereview(self):
        reviews = self.reviewrating_set.aggregate(average=Avg("rating"))
        avg = 0
        if reviews["average"] is not None:
            avg = float(reviews["average"])
        return avg


class ReviewRating(BaseModelWithUID):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey("core.User", on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.product.title
