from django.contrib import admin

from .models import Artwork, ArtworkImage, Bid, BidFinalization, Profile, Seller


class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    extra = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username', 'user__email')


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'seller_type', 'created_at')
    list_filter = ('seller_type',)
    search_fields = ('user__username', 'user__email', 'bio', 'address')


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'medium', 'style', 'price', 'year')
    list_filter = ('medium', 'style', 'year')
    search_fields = ('title', 'medium', 'style', 'provenance')
    inlines = (ArtworkImageInline,)


@admin.register(ArtworkImage)
class ArtworkImageAdmin(admin.ModelAdmin):
    list_display = ('artwork', 'sort_order', 'created_at')
    search_fields = ('artwork__title', 'alt_text')


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('artwork', 'bidder', 'price', 'expiration', 'status')
    list_filter = ('status', 'expiration')
    search_fields = ('artwork__title', 'bidder__username', 'bidder__email')


@admin.register(BidFinalization)
class BidFinalizationAdmin(admin.ModelAdmin):
    list_display = ('bid', 'created_at')
    search_fields = ('bid__artwork__title', 'bid__bidder__username', 'address')
