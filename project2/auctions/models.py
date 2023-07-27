from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    cateName = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f'{self.cateName}'

class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    price = models.FloatField()
    image = models.CharField(blank=False, max_length=1000, default="https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/1665px-No-Image-Placeholder.svg.png")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self) -> str:
        return f"{self.title}"


class Bid(models.Model):
    product = models.ForeignKey(Listing, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="BidUser")
    bid = models.FloatField()
    
    def __str__(self) -> str:
        return f"${self.bid} for {self.product} by {self.user}"


class Comment(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="userComment")
    content = models.CharField(max_length=300)
    product = models.ForeignKey(Listing, blank=True, null=True, on_delete=models.CASCADE, related_name="comment")

    def __str__(self) -> str:
        return f"Comment by {self.user} ({self.product})"

