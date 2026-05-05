from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Seller(models.Model):
    class SellerType(models.TextChoices):
        INDIVIDUAL = 'Individual', 'Individual'
        GALLERY = 'Gallery', 'Gallery'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seller_type = models.CharField(max_length=20, choices=SellerType.choices)
    address = models.TextField()
    logo = models.ImageField(
        upload_to='seller_logos/',
        blank=True,
        null=True,
    )
    cover = models.ImageField(
        upload_to='seller_covers/',
        blank=True,
        null=True,
    )
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} ({self.seller_type})'


class Artwork(models.Model):
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='artworks',
    )
    title = models.CharField(max_length=255)
    medium = models.CharField(max_length=120)
    style = models.CharField(max_length=120)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    dimensions = models.CharField(max_length=120)
    year = models.PositiveIntegerField()
    edition = models.CharField(max_length=120, blank=True)
    provenance = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ArtworkImage(models.Model):
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(upload_to='artwork_images/')
    alt_text = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return f'Image for {self.artwork}'


class Bid(models.Model):
    class BidStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        ACCEPTED = 'Accepted', 'Accepted'
        REJECTED = 'Rejected', 'Rejected'
        CONTINGENT = 'Contingent', 'Contingent'

    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name='bids',
    )
    bidder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bids',
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    expiration = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=BidStatus.choices,
        default=BidStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.bidder} bid {self.price} on {self.artwork}'


class BidFinalization(models.Model):
    bid = models.OneToOneField(
        Bid,
        on_delete=models.CASCADE,
        related_name='finalization',
    )
    address = models.TextField()
    payment_info = models.CharField(
        max_length=255,
        help_text='Store only non-sensitive payment references or summaries.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Finalization for {self.bid}'
