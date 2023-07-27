from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Bid, Comment  


def index(request):
    activeListing = Listing.objects.filter(isActive=True)
    cate = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listing": activeListing,
        "category": cate
    })


def create(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories
        })
    else:
        title = request.POST["title"]
        price = request.POST["price"]
        description = request.POST["description"]
        image = request.POST["url"]
        cate = request.POST['cate']
        owner = request.user
        newListing = Listing(
            title = title,
            description = description,
            price = price,
            image = image,
            category = Category.objects.get(cateName=cate),
            owner = owner
        )
        newListing.save()
        return HttpResponseRedirect(reverse("index"))
    


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
    

def sortCate(request):
    if request.method == "POST":
        category = request.POST['cate']
        activeListing = Listing.objects.filter(isActive=True, category = Category.objects.get(cateName=category))
        if activeListing.exists():
            cate = Category.objects.all()
            return render(request, 'auctions/index.html', {
            'category': cate,
            'listing': activeListing
        })
        else:
            return render(request, 'auctions/error.html', {
                "error": "Not found any listing !"
            })
        

def detail(request, id):
    listing = Listing.objects.get(pk=id)
    inWatchlist = request.user in listing.watchlist.all()
    bid = Bid.objects.all()
    comment = Comment.objects.filter(product=listing)
    BidWiner = Bid.objects.filter()
    return render(request, 'auctions/detail.html', {
        "listing": listing,
        "inWatchlist": inWatchlist,
        "amount": len(bid.filter(product=listing)),
        "allComment": comment,
    })

def removeFrom(request, id):
    listingData = Listing.objects.get(pk = id)
    CurrentUser = request.user
    listingData.watchlist.remove(CurrentUser)
    listingData.save()
    return HttpResponseRedirect(reverse("detail", args=[id]))

def addTo(request, id):
    listingData = Listing.objects.get(pk = id)
    CurrentUser = request.user
    listingData.watchlist.add(CurrentUser)
    listingData.save()
    return HttpResponseRedirect(reverse("detail", args=[id]))


def bid(request, id):
    listingData = Listing.objects.get(pk=id)
    bidAmount = int(request.POST['bidSubmit'])
    bid = Bid(
        product=listingData,
        user = request.user,
        bid=bidAmount
    )
    bid.save()
    condition = listingData.price < bidAmount
    if condition == True:
        listingData.price = bidAmount
        listingData.save()
        return HttpResponseRedirect(reverse("detail", args=[id]))
    else:
        return render(request, 'auctions/error.html', {
            "error": "Bid must be greater than the current price"
        })


def watchlist(request):
    listing = Listing.objects.filter(watchlist=request.user)
    cate = Category.objects.all()
    return render(request, 'auctions/watchlist.html', {
        "listing": listing,
        "category": cate
    })


def comment(request, id):
    listing = Listing.objects.get(pk=id)
    new_com = Comment(
        user = request.user,
        content = request.POST['content'],
        product = listing
    )
    new_com.save()
    return HttpResponseRedirect(reverse("detail", args=[id]))


def close(request, id):
    listing = Listing.objects.get(pk=id)
    listing.isActive = False
    listing.save()
    return HttpResponseRedirect(reverse("detail", args=[id]))