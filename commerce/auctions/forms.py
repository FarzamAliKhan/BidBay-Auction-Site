from .models import *
from django.forms import ModelForm


class ImageForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ('title','starting_bid','auction_category','description','thumbnail')

class BidForm(ModelForm):
    class Meta:
        model = Bids
        fields = ('bid_amount',)