from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache



from .models import User, AuctionListing, AuctionComments, Bids


def index(request):
    vehicles = AuctionListing.objects.filter(auction_category='Vehicles')[:4]
    mobiles = AuctionListing.objects.filter(auction_category='Mobile Phones')[:4]

    return render(request, "auctions/index.html", {
        'vehicles': vehicles,
        'mobiles':mobiles,
    })

def listing(request, pk):
    listing = AuctionListing.objects.get(id=pk)
    is_favourite= False

    if listing.current_bid:
        if listing.current_bid > 10000:
            min_bid = listing.current_bid + 50
        elif listing.current_bid > 1000:
            min_bid = listing.current_bid + 10
        else:
            min_bid = listing.current_bid + 2
    else:
        if listing.starting_bid > 10000:
            min_bid = listing.starting_bid + 50
        elif listing.starting_bid > 1000:
            min_bid = listing.starting_bid + 10
        elif listing.starting_bid > 0:
            min_bid = listing.starting_bid + 2
    
    if listing.favourite.filter(id=request.user.id).exists():
        is_favourite=True
    num_of_bids_registered =  listing.bids_registered.count()
    bids_registered = listing.bids_registered.all()
    
    time_left_in_ms = listing.get_time_left()

    accept_header = request.headers.get('Accept')
    
    if 'application/json' in accept_header:
        # Return JSON response
        data = {
            'time_left_in_ms': time_left_in_ms
        }
        return JsonResponse(data)
    else:
        # Return rendered HTML template
        return render(request, "auctions/listing.html", {
            'listing': listing,
            'is_favourite': is_favourite,
            'min_bid': min_bid,
            'num_bids_registered': num_of_bids_registered,
            'bids_registered': bids_registered,
            'time_left_in_ms': time_left_in_ms
        })
        
   

def validate_bid(request,pk):
    f = BidForm(request.POST)
    auction_listing = AuctionListing.objects.get(id=pk)

    if f.is_valid():
        bid = f.cleaned_data['bid_amount']
        auction_bid = f.save(commit=False)
        auction_bid.created_by = request.user
        auction_bid.bid_amount = bid
        auction_bid.listing = auction_listing
        auction_bid.save()

        auction_listing.bids_registered.add(auction_bid)
        auction_listing.current_bid = bid
        auction_listing.save()  # Save the updated auction_listing

        return redirect('listing', pk=pk)
    else:
        return redirect('listing', pk=pk)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    


@login_required
def add_listing(request):
    if request.method == "POST":
        f = ImageForm(request.POST, request.FILES)
        if f.is_valid():
            auction_listing = f.save(commit=False)
            auction_listing.created_by = request.user
            auction_listing.save()
            f_obj = f.instance #if instance already present
            return render(request, 'auctions/listing.html',{
                'listing':f_obj
            })
    else:
        f=ImageForm()
        return render(request,'auctions/add_listing.html',{
            'form':f
        })
    

def view_category(request, category_req):
    category = AuctionListing.objects.filter(auction_category=category_req)
    return render(request,"auctions/category_page.html",{
        "category":category,
        "category_req":category_req
    })

@login_required
@never_cache
def view_wishlist(request):
    user=request.user
    favourite_listings = user.favourite.all()
    return render(request, 'auctions/wishlist.html',{
        'favourite_listings':favourite_listings,
    })

@login_required
def wishlist_listing(request,pk):
    listing = get_object_or_404(AuctionListing, id=pk)
    if listing.favourite.filter(id=request.user.id).exists():
        listing.favourite.remove(request.user)
    else:
        listing.favourite.add(request.user)
    
    return HttpResponseRedirect(listing.get_absolute_url())

@never_cache
def delete_wishlist(request,pk):
    listing= AuctionListing.objects.get(id=pk)
    listing.favourite.remove(request.user)
    user=request.user
    favourite_listings = user.favourite.all()
    return render(request, 'auctions/wishlist.html',{
        'favourite_listings':favourite_listings,
    })
    
