from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from datetime import timedelta
from django.utils import timezone


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    CATEGORY = [
        ("Fashion","Fashion"),
        ("Toys & Games","Toys & Games"),
        ("Electronics","Electronics"),
        ("Mobile Phones","Mobile Phones"),
        ("Home","Home"),
        ("Sports & Outdoor", "Sports & Outdoor"),
        ("Vehicles", "Vehicles"),
        ("Beauty", "Beauty"),
        ("Furniture","Furniture"),
        ("Jewelry & Watches","Jewelry & Watches"),   
        ("Collectibles & Art","Collectibles & Art"),
        ("Music & Musical Instruments","Music & Musical Instruments")
    ]

    title = models.CharField(max_length=120, blank=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, editable=False, on_delete=models.CASCADE )
    date_posted = models.DateTimeField(auto_now_add=True)
    time_left = models.DurationField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    current_bid = models.IntegerField(null=True, blank=True)
    starting_bid = models.IntegerField(blank=False, validators=[MinValueValidator(1)])
    description = models.CharField(max_length=300 ,blank=False)
    auction_category= models.CharField( max_length=100 , choices=CATEGORY, blank=True)
    bids_registered = models.ManyToManyField('Bids', blank=True, related_name='listings' )
    favourite = models.ManyToManyField(User, related_name='favourite',blank=True)
    thumbnail = models.ImageField(blank=True, upload_to='images/')
    image2 = models.ImageField(blank=True, upload_to='images/')
    image3 = models.ImageField(blank=True, upload_to='images/')
    image4 = models.ImageField(blank=True, upload_to='images/')
    image5 = models.ImageField(blank=True, upload_to='images/')

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('listing', args=[str(self.id)])
    
    def get_time_left(self):
        # Calculate and set the end_time field when saving the listing
        self.end_time = self.date_posted + timedelta(days=20)   
        self.time_left = self.end_time - timezone.now()
        time_in_ms = self.time_left.total_seconds()*1000
        super(AuctionListing, self).save()
        return time_in_ms


class Bids(models.Model):
    created_by = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    bid_amount = models.IntegerField(blank=False)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_posted']

class AuctionComments(models.Model):
    created_by = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)