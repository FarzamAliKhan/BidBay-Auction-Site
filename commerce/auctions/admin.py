from django.contrib import admin
from .models import User, AuctionComments, AuctionListing, Bids


class AuctionListingAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by',)  # Make 'created_by' field read-only

admin.site.register(User)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(AuctionComments)
admin.site.register(Bids)

  