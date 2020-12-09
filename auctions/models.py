from django.contrib.auth.models import AbstractUser
from django.db import models


def upload_to(instance, filename):
    return 'images/%s/%s' % (instance.listing.id, filename)


class User(AbstractUser):
    pass


class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    desc = models.CharField(max_length=256)
    price = models.IntegerField()
    date_created = models.CharField(max_length=64)
    is_active = models.BooleanField()


class Image(models.Model):
    image = models.ImageField(upload_to=upload_to)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="image")


class CategoryA(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="is_cata")

    @staticmethod
    def get_id():
        return "CatA"


class CategoryB(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="is_catb")

    @staticmethod
    def get_id():
        return "CatB"


class CategoryC(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="is_catc")

    @staticmethod
    def get_id():
        return "CatC"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=512)
    date_added = models.IntegerField()

    class Meta:
        unique_together = ('author', 'listing', 'date_added')


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    value = models.IntegerField()


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'listing',)


CATEGORY_MODEL = {CategoryA.get_id(): CategoryA, CategoryB.get_id(): CategoryB,
                  CategoryC.get_id(): CategoryC}
